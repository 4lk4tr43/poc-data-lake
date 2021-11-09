include('./apps/collectors/file-loader/Tiltfile')
include('./apps/collectors/weather-tracking/Tiltfile')
include('./queues/kafka/Tiltfile')

docker_compose([
	'./service-descriptions/docker-compose.apps.collectors.file-loader.yml',
	'./service-descriptions/docker-compose.apps.collectors.weather-tracking.yml',
	'./service-descriptions/docker-compose.queues.kafka.yml',
	'./service-descriptions/docker-compose.data-lakes.hadoop.yml',
])
