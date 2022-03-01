import boto3

def detect_text(photo, bucket):

    client=boto3.client('rekognition')

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
    return len(textDetections)

def main():

    bucket='photos-for-golf-scoring'
    photo='score_card.jpg'
    text_count=detect_text(photo,bucket)
    print("Text detected: " + str(text_count))


if __name__ == "__main__":
    main()