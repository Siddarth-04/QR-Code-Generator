from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)

def make_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    content = request.form.get('content', '')
    if not content:
        return "No content", 400
    buf = make_qr(content)
    return send_file(buf, mimetype='image/png')

@app.route('/download')
def download():
    data = request.args.get('data', '')
    buf = make_qr(data)
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)
