#!/usr/bin/env python3

def fix_html_file():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the problematic section and remove it
    start_marker = "        // Add event listeners for application type to show/hide relevant sections"
    end_marker = "        // Add event listeners for sub-options"
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos != -1 and end_pos != -1:
        # Remove the problematic section
        new_content = content[:start_pos] + content[end_pos:]
        
        # Also remove the old sub-options event listeners
        old_sub_options_start = "        // Add event listeners for sub-options"
        old_sub_options_end = "    </script>"
        
        start_pos2 = new_content.find(old_sub_options_start)
        end_pos2 = new_content.find(old_sub_options_end)
        
        if start_pos2 != -1 and end_pos2 != -1:
            # Keep everything up to the old sub-options, then jump to the end
            final_content = new_content[:start_pos2] + "    </script>\n</body>\n</html>"
            
            with open('templates/index.html', 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print("Fixed the HTML file by removing duplicate event listeners")
            return True
    
    print("Could not find the problematic section")
    return False

if __name__ == "__main__":
    fix_html_file() 