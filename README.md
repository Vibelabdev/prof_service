# Сервис анализа социальных сетей для профориентации молодежи  

## Описание задачи

Разработайте сервис, который сможет анализировать активность пользователей в социальных сетях с целью определения их интересов, увлечений и потенциальных навыков для дальнейшего предложения наиболее подходящих профессий и образовательных путей. Сервис должен учитывать конфиденциальность данных и соответствовать нормативным требованиям по защите личной информации.

Протестировать сервис можно по ссылке: [ai-project-21.ru/docs](https://ai-project-21.ru/docs)

Для запуска сервиса необходим `service_token` для VK API, его можно получить, следуя инструкции в этой статье: [Гайд по API ВКонтакте](https://smmplanner.com/blog/gaid-po-api-vk-kak-podkliuchit-i-ispolzovat/).

### Команды для запуска

Запуск через pip:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 4000

Запуск через docker:

docker build -t app .
docker run -d -p 80:4000 app
