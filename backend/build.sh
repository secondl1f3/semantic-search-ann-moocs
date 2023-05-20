#!/bin/bash
docker build --no-cache -t tech-courses-search-engine-backend:latest .
docker push tech-courses-search-engine-backend:latest