# Local Run Notes

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Confirm PostgreSQL database `e_commerce` exists and `e_commerce/settings.py` credentials match your local setup.
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

