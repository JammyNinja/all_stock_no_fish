build_backend_local:
#  execute from project root
	docker build -t $(DOCKER_IMAGE_NAME) -f Dockerfile .

build_backend_cloud:
	docker build -t $(IMAGE_URI) -f Dockerfile .

push_docker_image:
	docker push $(IMAGE_URI)

run_docker_local:
	docker run -it \
		-p 8000:8080 \
		-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/key.json \
		-v $(GOOGLE_APPLICATION_CREDENTIALS):/secrets/key.json \
		$(DOCKER_IMAGE_NAME)


run_local_all:
	streamlit run frontend/app.py
