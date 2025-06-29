from flask import Flask, render_template, request, send_file, jsonify
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os
from datetime import datetime

app = Flask(__name__)

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
            'main_applicant_category': main_applicant_category,
            'is_expedited_allowed': is_expedited,
            'expedited_reason': expedited_reason,
            'title': form_data.get('title', ''),
            'noOfClaims': form_data.get('noOfClaims', '0'),
            'noOfDrawings': form_data.get('noOfDrawings', '0'),
            'sheet_counts': {
                'patent_document': form_data.get('sheetCounts[patentDocumentSheets]', '0'),
                'abstract': form_data.get('sheetCounts[abstractSheets]', '0'),
                'claims': form_data.get('sheetCounts[claimsSheets]', '0'),
                'drawings': form_data.get('sheetCounts[drawingSheets]', '0')
            },
            'publication_preference': form_data.get('publicationPreference', 'Ordinary'),
            'examination_preference': form_data.get('examinationPreference', 'Ordinary'),
            'agents': agents,
            'agent1_no': agents[0]['inpa_no'] if len(agents) > 0 else '',
            'agent1_name': agents[0]['name'] if len(agents) > 0 else '',
            'agent1_mobile': agents[0]['mobile'] if len(agents) > 0 else '',
            'agent2_no': agents[1]['inpa_no'] if len(agents) > 1 else '',
            'agent2_name': agents[1]['name'] if len(agents) > 1 else '',
            'agent2_mobile': agents[1]['mobile'] if len(agents) > 1 else '',
            'fees': fees,
            'total_fee': sum(fees.values()),
            'date': datetime.now().strftime("%d/%m/%Y"),
            # Only keep checkboxes for Provisional/Complete
            'cb_type_provisional': get_checkbox_symbol(application_type == 'Provisional'),
            'cb_type_complete': get_checkbox_symbol(application_type == 'Complete'),
            # Category of Applicant checkboxes based on the main category
            'cb_category_natural': get_checkbox_symbol(main_applicant_category == 'Natural Person'),
            'cb_category_small': get_checkbox_symbol(main_applicant_category == 'Small Entity'),
            'cb_category_startup': get_checkbox_symbol(main_applicant_category == 'Start-Up'),
            'cb_category_others': get_checkbox_symbol(main_applicant_category == 'Others'),
            'cb_category_educational': get_checkbox_symbol(main_applicant_category == 'Educational institution'),
            
            # Inventors same as applicants
            'cb_inventors_same_yes': get_checkbox_symbol(form_data.get('inventorsSameAsApplicants') == 'Yes'),
            'cb_inventors_same_no': get_checkbox_symbol(form_data.get('inventorsSameAsApplicants') == 'No'),
            
            # Convention Application Details
            'convention_country': form_data.get('conventionCountry', ''),
            'convention_number': form_data.get('conventionNumber', ''),
            'convention_date': form_data.get('conventionDate', ''),
            'convention_applicant': form_data.get('conventionApplicant', ''),
            'convention_title': form_data.get('conventionTitle', ''),
            'convention_ipc': form_data.get('conventionIPC', ''),
            
            # PCT Application Details
            'pct_number': form_data.get('pctNumber', ''),
            'pct_date': form_data.get('pctDate', ''),
            
            # Divisional Application Details
            'divisional_number': form_data.get('divisionalNumber', ''),
            'divisional_date': form_data.get('divisionalDate', ''),
            
            # Patent of Addition Details
            'addition_number': form_data.get('additionNumber', ''),
            'addition_date': form_data.get('additionDate', ''),
            
            'service_address': {
                'name': form_data.get('serviceAddress[serviceName]', ''),
                'postal_address': form_data.get('serviceAddress[postalAddress]', ''),
                'telephone': form_data.get('serviceAddress[telephone]', ''),
                'mobile': form_data.get('serviceAddress[mobile]', ''),
                'fax': form_data.get('serviceAddress[fax]', ''),
                'email': form_data.get('serviceAddress[email]', ''),
            }
        }
        
        app.logger.info("Context prepared successfully")
        
        # Render the template
        try:
            doc.render(context)
            app.logger.info("Template rendered successfully")
        except Exception as e:
            app.logger.error(f"Error rendering template: {str(e)}")
            raise
        
        # Save the document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"patent_application_{timestamp}.docx"
        doc.save(filename)
        app.logger.info(f"Document saved as {filename}")
        
        return filename
    except Exception as e:
        app.logger.error(f"Error in generate_document: {str(e)}")
        raise

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = request.form.to_dict()
        app.logger.info(f"Received form data: {form_data}")

        # Map 'provisionalOrComplete' to 'applicationType' if 'applicationType' is missing
        if 'applicationType' not in form_data and 'provisionalOrComplete' in form_data:
            form_data['applicationType'] = form_data['provisionalOrComplete']

        # Validate required fields
        required_fields = ['applicationType', 'title']
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Ensure at least one inventor is present
        if not any(key.startswith('inventors[') for key in form_data.keys()):
            return jsonify({'error': 'At least one inventor is required'}), 400
        
        # Ensure at least one applicant is present
        has_applicant = False
        i = 0
        while f'applicants[{i}][name]' in form_data:
            if form_data[f'applicants[{i}][name]']:
                has_applicant = True
                break
            i += 1
        
        if not has_applicant:
            return jsonify({'error': 'At least one applicant is required'}), 400
        
        # Ensure agent details are present
        agent_fields = ['agents[0][inpaNo]', 'agents[0][name]', 'agents[0][mobile]', 'agents[0][email]']
        for field in agent_fields:
            if field not in form_data or not form_data[field]:
                return jsonify({'error': f'Missing required agent field: {field}'}), 400
        
        # Ensure service address details are present
        service_fields = ['serviceAddress[serviceName]', 'serviceAddress[postalAddress]', 'serviceAddress[mobile]', 'serviceAddress[email]']
        for field in service_fields:
            if field not in form_data or not form_data[field]:
                return jsonify({'error': f'Missing required service address field: {field}'}), 400
        
        # Validate applicant categories
        allowed_categories = [
            'Natural Person',
            'Small Entity',
            'Start-Up',
            'Educational institution',
            'Others'
        ]
        for key in form_data:
            if key.endswith('[category]') and form_data[key] not in allowed_categories and form_data[key] != '':
                return jsonify({'error': f'Invalid applicant category: {form_data[key]}'}), 400
        
        # Generate the document
        try:
            filename = generate_document(form_data)
            app.logger.info(f"Document generated successfully: {filename}")
            return send_file(filename, as_attachment=True)
        except Exception as e:
            app.logger.error(f"Error generating document: {str(e)}")
            return jsonify({'error': f'Error generating document: {str(e)}'}), 500
            
    except Exception as e:
        app.logger.error(f"Error processing form submission: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/application-details', methods=['GET'])
def application_details():
    return render_template('application_details.html')

@app.route('/calculate-fees', methods=['POST'])
def calculate_fees_api():
    data = request.get_json()
    
    # Calculate total sheets
    total_sheets = sum(data['sheetCounts'].values())
    
    # Calculate excess sheet fee
    excess_sheet_fee = 0
    if total_sheets > 30:
        excess_sheet_fee = (total_sheets - 30) * 160  # ₹160 per excess sheet
    
    # Calculate excess claim fee
    excess_claim_fee = 0
    if data['others']['noOfClaims'] > 10:
        excess_claim_fee = (data['others']['noOfClaims'] - 10) * 800  # ₹800 per excess claim
    
    return jsonify({
        'excessSheetFee': {
            'online': excess_sheet_fee,
            'offline': int(excess_sheet_fee * 1.1)  # 10% more for offline
        },
        'excessClaimFee': {
            'online': excess_claim_fee,
            'offline': int(excess_claim_fee * 1.1)  # 10% more for offline
        }
    })

def get_main_applicant_category(applicants):
    max_priority = 0
    main_category = None
    for applicant in applicants:
        cat = applicant.get("category")
        priority = CATEGORY_PRIORITY.get(cat, 0)
        if priority > max_priority:
            max_priority = priority
            main_category = cat
    return main_category

def is_expedited_allowed(applicants):
    """
    applicants: List[Dict] -> [{'name': 'A', 'category': 'Start-Up', 'gender': 'Female'}, ...]
    returns: Tuple[bool, Optional[str]]
    """
    for applicant in applicants:
        category = applicant.get('category')
        gender = applicant.get('gender', '').lower()
        # Eligible by category
        if category in EXPEDITED_ELIGIBLE_CATEGORIES:
            return True, None
        # Eligible by gender (if natural person and female)
        if category == "Natural Person" and gender == "female":
            return True, None
    # Not eligible
    return False, "Expedited examination not available – no eligible applicant (Start-Up, Small Entity, Educational Institution, or Female Natural Person)."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 
