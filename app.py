from flask import Flask, render_template, request, send_file, jsonify
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import drafting module components
from database import init_database, create_indexes
from drafting_routes import drafting_bp
from config import config

app = Flask(__name__)

# Configure the app
config_name = os.getenv('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])

# Initialize database
init_database(app)

# Register blueprints
app.register_blueprint(drafting_bp)

# Create database indexes
with app.app_context():
    create_indexes()

# Priority for deciding main entity (higher means higher fee)
CATEGORY_PRIORITY = {
    "Others": 5,
    "Educational institution": 4,
    "Start-Up": 3,
    "Small Entity": 2,
    "Natural Person": 1
}

# Fee table for each applicant category (example values, update as per official rules)
CATEGORY_FEES = {
    'Natural Person': {
        'filing_fee': 1600,
        'publication_fee': 2500,
        'examination_fee': 4000
    },
    'Small Entity': {
        'filing_fee': 4000,
        'publication_fee': 6250,
        'examination_fee': 10000
    },
    'Start-Up': {
        'filing_fee': 1600,
        'publication_fee': 2500,
        'examination_fee': 4000
    },
    'Educational institution': {
        'filing_fee': 8000,
        'publication_fee': 10000,
        'examination_fee': 20000
    },
    'Others': {
        'filing_fee': 8000,
        'publication_fee': 12500,
        'examination_fee': 20000
    }
}

EXPEDITED_ELIGIBLE_CATEGORIES = {
    "Start-Up",
    "Small Entity",
    "Educational institution"
}

def calculate_fees(form_data):
    # Base fees
    fees = {
        'filing_fee': 0,
        'publication_fee': 0,
        'examination_fee': 0,
        'excess_sheet_fee': 0,
        'excess_claim_fee': 0
    }
    
    # Calculate total sheets
    total_sheets = (
        int(form_data.get('sheetCounts[patentDocumentSheets]', 0)) +
        int(form_data.get('sheetCounts[abstractSheets]', 0)) +
        int(form_data.get('sheetCounts[claimsSheets]', 0)) +
        int(form_data.get('sheetCounts[drawingSheets]', 0))
    )
    
    # Calculate excess sheet fee (₹160 per excess sheet after 30 sheets)
    if total_sheets > 30:
        fees['excess_sheet_fee'] = (total_sheets - 30) * 160
    
    # Calculate excess claim fee (₹800 per excess claim after 10 claims)
    no_of_claims = int(form_data.get('sheetCounts[claimsSheets]', 0))
    if no_of_claims > 10:
        fees['excess_claim_fee'] = (no_of_claims - 10) * 800
    
    # Use main_applicant_category for fee logic
    main_applicant_category = form_data.get('main_applicant_category')
    category_fees = CATEGORY_FEES.get(main_applicant_category, CATEGORY_FEES['Others'])
    
    # Filing fee calculation
    if form_data['applicationType'] == 'Provisional':
        fees['filing_fee'] = category_fees['filing_fee']  # Provisional filing fee (same as base for category)
    else:  # Complete application
        fees['filing_fee'] = category_fees['filing_fee']  # Complete filing fee (same as base for category)
        
        # Publication fee
        if form_data.get('publicationPreference') == 'Early':
            fees['publication_fee'] = category_fees['publication_fee']
        else:
            fees['publication_fee'] = 0
        
        # Examination fee
        if form_data.get('examinationPreference') == 'Expedited':
            fees['examination_fee'] = category_fees['examination_fee']
        else:
            # Ordinary examination fee (could be different, update if needed)
            fees['examination_fee'] = category_fees['examination_fee']
    
    return fees

def generate_document(form_data):
    try:
        doc = DocxTemplate("form1_template.docx")
        app.logger.info("Template loaded successfully")
        
        # Helper function to convert boolean to checkbox symbol
        def get_checkbox_symbol(value):
            return '☑' if value else '☐'
        
        # Process inventors data
        inventors = []
        i = 0
        while f'inventors[{i}][name]' in form_data:
            inventor = {
                'name': form_data[f'inventors[{i}][name]'],
                'gender': form_data[f'inventors[{i}][gender]'],
                'nationality': form_data[f'inventors[{i}][nationality]'],
                'residency': form_data[f'inventors[{i}][residency]'],
                'address': form_data[f'inventors[{i}][address]']
            }
            if inventor['residency'] == 'India':
                inventor['state'] = form_data.get(f'inventors[{i}][state]', '')
            inventors.append(inventor)
            i += 1
        
        app.logger.info(f"Processed {len(inventors)} inventors")
        
        # Process applicants data
        applicants = []
        i = 0
        while f'applicants[{i}][name]' in form_data:
            name = form_data.get(f'applicants[{i}][name]')
            if name: # Ensure there is an applicant
                applicant = {
                    'name': name,
                    'gender': form_data.get(f'applicants[{i}][gender]', ''),
                    'category': form_data.get(f'applicants[{i}][category]', 'Others'),
                    'nationality': form_data.get(f'applicants[{i}][nationality]', ''),
                    'residency': form_data.get(f'applicants[{i}][residency]', ''),
                    'address': form_data.get(f'applicants[{i}][address]', '')
                }
                if applicant['residency'] == 'India':
                    applicant['state'] = form_data.get(f'applicants[{i}][state]', '')
                applicants.append(applicant)
            i += 1
        
        app.logger.info(f"Processed {len(applicants)} applicants")
        
        # Process multiple agents
        agents = []
        i = 0
        while f'agents[{i}][inpaNo]' in form_data:
            if form_data.get(f'agents[{i}][inpaNo]') or form_data.get(f'agents[{i}][name]'):
                agents.append({
                    'inpa_no': form_data.get(f'agents[{i}][inpaNo]', ''),
                    'name': form_data.get(f'agents[{i}][name]', ''),
                    'mobile': form_data.get(f'agents[{i}][mobile]', ''),
                    'email': form_data.get(f'agents[{i}][email]', ''),
                })
            i += 1
        
        # Calculate fees
        fees = calculate_fees(form_data)
        
        # Create default empty inventor and applicant if none exist
        default_inventor = {
            'name': '',
            'gender': '',
            'nationality': '',
            'residency': '',
            'address': '',
            'state': ''
        }
        
        default_applicant = {
            'name': '',
            'category': '',
            'nationality': '',
            'residency': '',
            'address': '',
            'state': ''
        }
        
        # Only use applicationType as Provisional or Complete
        application_type = form_data.get('applicationType', '')
        
        # After applicants are processed and before context is built:
        main_applicant_category = get_main_applicant_category(applicants)
        is_expedited, expedited_reason = is_expedited_allowed(applicants)
        
        context = {
            'application_type': application_type,
            'previous_provisional': form_data.get('previousProvisionalFiled', 'No'),
            'provisional_number': form_data.get('provisionalApplicationNumber', ''),
            'inventors': inventors,
            'inventor': inventors[0] if inventors else default_inventor,  # Use default if no inventors
            'applicants': applicants,
            'applicant': applicants[0] if applicants else default_applicant,  # Use default if no applicants
            'agents': agents,
            'agent': agents[0] if agents else {'inpa_no': '', 'name': '', 'mobile': '', 'email': ''},
            'main_applicant_category': main_applicant_category,
            'is_expedited': is_expedited,
            'expedited_reason': expedited_reason,
            'fees': fees,
            'total_fee': sum(fees.values()),
            'sheet_counts': {
                'patent_document_sheets': form_data.get('sheetCounts[patentDocumentSheets]', 0),
                'abstract_sheets': form_data.get('sheetCounts[abstractSheets]', 0),
                'claims_sheets': form_data.get('sheetCounts[claimsSheets]', 0),
                'drawing_sheets': form_data.get('sheetCounts[drawingSheets]', 0)
            },
            'publication_preference': form_data.get('publicationPreference', ''),
            'examination_preference': form_data.get('examinationPreference', ''),
            'checkbox_previous_provisional': get_checkbox_symbol(form_data.get('previousProvisionalFiled') == 'Yes'),
            'checkbox_publication_early': get_checkbox_symbol(form_data.get('publicationPreference') == 'Early'),
            'checkbox_examination_expedited': get_checkbox_symbol(form_data.get('examinationPreference') == 'Expedited')
        }
        
        app.logger.info("Context built successfully")
        
        # Render the template
        doc.render(context)
        app.logger.info("Template rendered successfully")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"patent_application_{timestamp}.docx"
        
        # Save the document
        doc.save(filename)
        app.logger.info(f"Document saved as {filename}")
        
        return filename
        
    except Exception as e:
        app.logger.error(f"Error generating document: {str(e)}")
        raise

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/drafting', methods=['GET'])
def drafting():
    """Route to the AI-powered patent drafting interface"""
    return render_template('drafting.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = request.form.to_dict()
        app.logger.info("Form data received")
        
        # Generate the document
        filename = generate_document(form_data)
        
        # Send the file
        return send_file(filename, as_attachment=True, download_name=filename)
        
    except Exception as e:
        app.logger.error(f"Error in submit: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/application-details', methods=['GET'])
def application_details():
    return render_template('application_details.html')

@app.route('/calculate-fees', methods=['POST'])
def calculate_fees_api():
    try:
        form_data = request.get_json()
        fees = calculate_fees(form_data)
        total_fee = sum(fees.values())
        
        return jsonify({
            'fees': fees,
            'total_fee': total_fee
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_main_applicant_category(applicants):
    """Determine the main applicant category for fee calculation"""
    if not applicants:
        return "Others"
    
    # Find the applicant with the highest priority (lowest number)
    main_applicant = min(applicants, key=lambda x: CATEGORY_PRIORITY.get(x.get('category', 'Others'), 5))
    return main_applicant.get('category', 'Others')

def is_expedited_allowed(applicants):
    """Check if expedited examination is allowed for the applicants"""
    if not applicants:
        return False, "No applicants found"
    
    # Check if any applicant is eligible for expedited examination
    eligible_applicants = [app for app in applicants if app.get('category') in EXPEDITED_ELIGIBLE_CATEGORIES]
    
    if eligible_applicants:
        return True, f"Eligible: {', '.join([app.get('category') for app in eligible_applicants])}"
    else:
        return False, "No eligible applicants for expedited examination"

if __name__ == '__main__':
    app.run(debug=True) 
