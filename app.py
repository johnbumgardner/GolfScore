import boto3

bucket='photos-for-golf-scoring'

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

def main():
    photo='score_card.jpg'
    text_count = detect_text(photo)
    player1 = text_count[0:9]
    player2 = text_count[10:18]
    sum1 = sum_player(player1)
    sum2 = sum_player(player2)
    print(sum1)
    print(sum2)

if __name__ == "__main__":
    main()