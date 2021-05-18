# Engine
Engine of Robster project

## Requirements
* Python 3.6 <= required
* requirements.txt
* gRPC

## Usage
1. Request APK file over gRPC communication (port: 50051) <AnalysisRequest>
2. wait for response (normally, about 1-2 seconds for analyze 20MB APK file)
3. Response when analysis process complete.
