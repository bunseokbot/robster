# Robster
Rob your precious machine learning model

@austinkim

## Introduction
This project was developed for detect and extract from mobile application (APK only)<br>
Currently, only static analysis method is supported.<br><br>
See the detail description in blog (Korean) - https://iam.namjun.kim/research/2021/02/24/rob-your-precious-machine-learning-model/

## Features
### Detection
* File signature matching
* static DEX (dalvik execution format) file method call trace

### Extraction
* Extract model using file scanning (signature matching)

## Phases
### Engine
Engine for detect and extract the ML model.

### Backend
The HTTP API server for connecting between robster-engine and end user.

### Frontend
TO-DO

## Supported ML libraries
* Tensorflow Lite (Tensorflow, Detect and extraction)
* Tesseract (Google, Detect only)
* Ncnn (Tencent, Detect only)
* MNN (Alibaba, Detect only)
* Caffe (Berkeley AI Research, Detect only)

## Pre-requirements
* Docker
* docker-compose

## How to use
Run command
```
docker-compose up -d
```

## Reference
The inspiration for this project is coming from this paper.
* Zhichuang Sun, Ruimin Sun, and Long Lu, "Mind Your Weight(s): A Large-scale Study on Insufficient Machine Learning Model Protection in Mobile Apps", arXiv:2002.07687

