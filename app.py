import boto3
from flask import Flask, request, jsonify
from PIL import Image


bucket='photos-for-golf-scoring'
app = Flask(__name__)

@app.route("/detect_text", methods=["POST"])
def process_image():
    file = request.files['image']
    img = Image.open(file.stream)
    img.save("score_card.jpg")
    text = detect_text("score_card.jpg")
    player1 = text[0:9]
    player2 = text[10:18]
    sum1 = sum_player(player1)
    sum2 = sum_player(player2)
    return jsonify({'msg': 'success', 'player1_score': sum1, 'player2_score': sum2})


def detect_text(photo):
    s3 = boto3.resource('s3')
    client=boto3.client('rekognition')

    s3.meta.client.upload_file(photo, bucket, photo)
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    text_detections=response['TextDetections']
    all_detected_chars = []    
    for entry in text_detections:
        text = entry['DetectedText']
        for ch in text:
            if not ch == ' ':
                all_detected_chars.append(ch)
        
    return all_detected_chars[0:18]

def sum_player(scores):
    sum = 0
    for i in scores:
        sum += int(i)
    return sum

if __name__ == "__main__":
    app.run(debug=True)