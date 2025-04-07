from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

def extract_video_id(url):
    if 'shorts' in url:
        return url.split('/')[-1]
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query).get('v', [None])[0]

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        full_text = ' '.join([entry['text'] for entry in transcript])
        return jsonify({'transcript': full_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
