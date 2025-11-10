# Настройка Google OAuth для входа через Google SSO

## Шаг 1: Создание OAuth 2.0 Client ID в Google Cloud Console

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Перейдите в **APIs & Services** → **Credentials**
4. Нажмите **Create Credentials** → **OAuth client ID**
5. Если это первый раз, настройте OAuth consent screen:
   - Выберите **External** (для тестирования)
   - Заполните обязательные поля (App name, User support email, Developer contact)
   - Добавьте scopes: `email`, `profile`
   - Добавьте test users (ваш email)
6. Создайте OAuth client ID:
   - Application type: **Web application**
   - Name: **Kanban Board** (или любое другое)
   - Authorized JavaScript origins:
     - Для локальной разработки: `http://localhost:8000`
     - Для Railway: `https://your-app.railway.app`
   - Authorized redirect URIs:
     - Для локальной разработки: `http://localhost:8000/accounts/google/login/callback/`
     - Для Railway: `https://your-app.railway.app/accounts/google/login/callback/`
7. Скопируйте **Client ID** и **Client Secret**

## Шаг 2: Настройка переменных окружения

### Для локальной разработки (.env файл):

```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
```

### Для Railway:

1. Откройте ваш сервис в Railway
2. Перейдите в **Variables**
3. Добавьте переменные:
   - `GOOGLE_OAUTH_CLIENT_ID` = ваш Client ID
   - `GOOGLE_OAUTH_CLIENT_SECRET` = ваш Client Secret

## Шаг 3: Выполнение миграций

После добавления поля `user` в модель Task:

```bash
# Локально
python manage.py makemigrations
python manage.py migrate

# В Docker
docker exec canban-web-1 python manage.py makemigrations
docker exec canban-web-1 python manage.py migrate
```

## Шаг 4: Создание Site в Django Admin

Django allauth требует настройку Site:

1. Запустите сервер
2. Откройте `/admin`
3. Войдите как суперпользователь (создайте через `python manage.py createsuperuser` если нужно)
4. Перейдите в **Sites** → **Sites**
5. Измените существующий site:
   - **Domain name**: `localhost:8000` (для разработки) или ваш Railway домен (например, `canban-production-e108.up.railway.app`)
   - **Display name**: `Kanban Board`
6. Сохраните

Или через Django shell:

```python
from django.contrib.sites.models import Site
site = Site.objects.get_current()
site.domain = 'your-domain.railway.app'  # или localhost:8000
site.name = 'Kanban Board'
site.save()
```

## Шаг 4.5: Настройка Social Application (альтернативный способ)

Если переменные окружения не работают, можно настроить через админку:

1. В Django Admin перейдите в **Social applications** → **Social applications**
2. Нажмите **Add social application**
3. Заполните:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: ваш Client ID
   - **Secret key**: ваш Client Secret
   - **Sites**: выберите ваш site
4. Сохраните

## Шаг 5: Проверка работы

1. Откройте приложение
2. Нажмите "Login with Google"
3. Выберите Google аккаунт
4. Разрешите доступ
5. Вы должны быть перенаправлены обратно на главную страницу
6. Теперь вы видите только свои задачи

## Важные замечания

- **Для production**: Убедитесь, что OAuth consent screen опубликован (не в режиме тестирования)
- **Redirect URIs**: Должны точно совпадать с настройками в Google Console
- **HTTPS**: В production Railway автоматически использует HTTPS
- **Существующие задачи**: Задачи без пользователя (если они есть) нужно будет назначить вручную через админку

## Troubleshooting

### Ошибка "redirect_uri_mismatch"
- Проверьте, что redirect URI в Google Console точно совпадает с вашим доменом
- Для Railway: `https://your-app.railway.app/accounts/google/login/callback/`

### Ошибка "access_denied"
- Убедитесь, что ваш email добавлен в test users в OAuth consent screen
- Или опубликуйте приложение (для production)

### Задачи не отображаются
- Убедитесь, что миграции выполнены
- Проверьте, что задачи привязаны к пользователю (через админку)

