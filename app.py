from flask import Flask, render_template, request, send_file
from conversion import file_conversion
import os

app = Flask(__name__)

# Define a directory to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'
# Define a directory to store converted files
app.config['CONVERTED_FOLDER'] = 'file_converted'

# Ensure the UPLOAD_FOLDER and CONVERTED_FOLDER exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['CONVERTED_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an input file is provided
        if 'input_file' not in request.files:
            message = "No input file provided."
            return render_template('index.html', message=message)

        input_file = request.files['input_file']
        output_format = request.form.get('output_format')
        output_file_name = request.form.get('output_file_name')

        # Check if the input file is empty
        if input_file.filename == '':
            message = "No selected input file."
            return render_template('index.html', message=message)

        # Check if the file extension is allowed
        if not allowed_file(input_file.filename):
            message = "Invalid input file format. Supported formats are .po, .xml, and .xlsx."
            return render_template('index.html', message=message)

        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file.filename)
        input_file.save(input_file_path)

        if output_format not in ('po', 'xml', 'xlsx'):
            message = "Invalid output file format. Supported formats are 'po', 'xml', and 'xlsx'."
            return render_template('index.html', message=message)

        # Call the conversion function from conversion.py based on the selected format
        output_file_path = file_conversion(input_file_path, output_format, output_file_name)

        return send_file(output_file_path, as_attachment=True)

    return render_template('index.html', message='')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'po', 'xml'}

if __name__ == "__main__":
    app.run(debug=True)
