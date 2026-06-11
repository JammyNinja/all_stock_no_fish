build_backend_local:
#  execute from project root
	docker build -t $(DOCKER_IMAGE_NAME) -f Dockerfile .

build_backend_cloud:
	docker build -t $(IMAGE_URI) -f Dockerfile .

push_docker_image:
	docker push $(IMAGE_URI)
