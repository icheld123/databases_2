import uuid
from faker import Faker
from datetime import datetime, timedelta
import random

# Configuración de Faker para nombres en español
fake = Faker('es_ES')
fake.unique.clear()  # Limpiar cache de nombres únicos

def generate_sql_file():
    # Crear archivo SQL
    with open('generate_data_corrected.sql', 'w', encoding='utf-8') as f:
        # Encabezado del archivo
        f.write("-- Script generado automáticamente con Python y Faker\n")
        f.write(f"-- Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 1. Crear tabla temporal con UUIDs para todas las entidades
        f.write("-- TABLA TEMPORAL CON UUID PARA TODAS LAS ENTIDADES\n")
        f.write("CREATE TEMP TABLE uuid_temp_entities AS\n")
        f.write("SELECT \n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_user,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_book,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_author,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_publisher,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_review,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_favorite,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_follow,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_reading_list,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_subscription,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_notification,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_promotion,\n")
        f.write("    md5(random()::text || clock_timestamp()::text || row_number() OVER ())::uuid AS id_ad_campaign,\n")
        f.write("    row_number() OVER () AS rn\n")
        f.write("FROM generate_series(1, 100000);\n\n")
        
        # 2. Insertar datos en tablas catálogo
        f.write("-- ============ DATOS DE CATÁLOGO ============\n")
        f.write("-- Resetear secuencias y forzar IDs conocidos\n")
        f.write("ALTER SEQUENCE user_type_user_type_id_seq RESTART WITH 1;\n")
        f.write("INSERT INTO \"user_type\" (\"user_type_id\", \"description\") VALUES\n")
        f.write("    (1, 'Administrador'), (2, 'Usuario Premium'), (3, 'Usuario Regular');\n")
        
        f.write("INSERT INTO \"plan_type\" (\"description\") VALUES\n")
        f.write("    ('Básico'), ('Premium'), ('Premium Plus');\n\n")
        
        f.write("INSERT INTO \"payment_status_type\" (\"description\") VALUES\n")
        f.write("    ('Pendiente'), ('Pagado'), ('Cancelado'), ('Rechazado');\n\n")
        
        f.write("INSERT INTO \"notification_type\" (\"description\") VALUES\n")
        f.write("    ('Nuevo libro'), ('Recordatorio'), ('Promoción'), ('Seguimiento');\n\n")
        
        f.write("INSERT INTO \"genre_type\" (\"description\") VALUES\n")
        f.write("    ('Ficción'), ('No ficción'), ('Misterio'), ('Romance'),\n")
        f.write("    ('Ciencia ficción'), ('Fantasía'), ('Biografía'), ('Historia');\n\n")
        
        f.write("INSERT INTO \"tag\" (\"description\") VALUES\n")
        f.write("    ('Bestseller'), ('Nuevo'), ('Recomendado'),\n")
        f.write("    ('Clásico'), ('Trending'), ('Award Winner');\n\n")
        
        # 3. Generar autores
        f.write("-- ============ GENERACIÓN DE AUTORES ============\n")
        f.write("-- Tabla temporal con biografías de autores\n")
        f.write("CREATE TEMP TABLE temp_author_bios AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    bio\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 500 biografías de autores
        batch_size = 100
        total_bios = 500
        
        for i in range(0, total_bios, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_bios:
                    break
                bio = f"Biografía de {fake.name()}. {fake.paragraph(nb_sentences=3)}".replace("'", "''")
                batch.append(f"        ('{bio}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_bios:
                f.write(",\n")
        
        f.write("\n    ) AS bios(bio);\n\n")
        
        f.write("-- Tabla temporal con nombres de autores\n")
        f.write("CREATE TEMP TABLE temp_author_names AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    name\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 1000 nombres de autores
        total_names = 1000
        
        for i in range(0, total_names, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_names:
                    break
                name = fake.name()[:40].replace("'", "''")
                batch.append(f"        ('{name}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_names:
                f.write(",\n")
        
        f.write("\n    ) AS names(name);\n\n")
        
        f.write("INSERT INTO public.\"author\" (\n")
        f.write("    author_id, \"name\", biography, nationality\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_author,\n")
        f.write("    an.name,\n")
        f.write("    ab.bio,\n")
        f.write("    (random() * 229 + 1)::int -- País aleatorio entre 1 y 230\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("JOIN temp_author_names an ON (random() * 999 + 1)::int = an.rn\n")
        f.write("JOIN temp_author_bios ab ON (random() * 499 + 1)::int = ab.rn;\n\n")
        
        # 4. Generar editoriales
        f.write("-- ============ GENERACIÓN DE EDITORIALES ============\n")
        f.write("-- Tabla temporal con nombres de editoriales\n")
        f.write("CREATE TEMP TABLE temp_publisher_names AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    name\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 1000 nombres de editoriales
        total_publishers = 1000
        
        for i in range(0, total_publishers, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_publishers:
                    break
                name = f"{fake.company()[:35]} Editorial".replace("'", "''")
                batch.append(f"        ('{name}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_publishers:
                f.write(",\n")
        
        f.write("\n    ) AS publishers(name);\n\n")
        
        f.write("-- Tabla temporal con descripciones de editoriales\n")
        f.write("CREATE TEMP TABLE temp_publisher_descs AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    descripcion\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 500 descripciones de editoriales
        total_descs = 500
        
        for i in range(0, total_descs, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_descs:
                    break
                desc = f"Editorial especializada en {random.choice(['ficción', 'no ficción', 'literatura técnica', 'libros académicos', 'poesía', 'teatro'])}".replace("'", "''")
                batch.append(f"        ('{desc}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_descs:
                f.write(",\n")
        
        f.write("\n    ) AS descs(descripcion);\n\n")
        
        f.write("-- Tabla temporal con websites de editoriales\n")
        f.write("CREATE TEMP TABLE temp_publisher_websites AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    website\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 500 websites
        total_websites = 500
        
        for i in range(0, total_websites, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_websites:
                    break
                website = f"https://www.{fake.domain_word()}.com".replace("'", "''")
                batch.append(f"        ('{website}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_websites:
                f.write(",\n")
        
        f.write("\n    ) AS websites(website);\n\n")
        
        f.write("INSERT INTO public.\"publisher\" (\n")
        f.write("    publisher_id, \"name\", country_id, founded_year, website, description\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_publisher,\n")
        f.write("    pn.name,\n")
        f.write("    (random() * 229 + 1)::int, -- País aleatorio entre 1 y 230\n")
        f.write("    (1800 + random() * 223)::int, -- Año entre 1800 y 2023\n")
        f.write("    pw.website,\n")
        f.write("    pd.descripcion\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("JOIN temp_publisher_names pn ON (random() * 999 + 1)::int = pn.rn\n")
        f.write("JOIN temp_publisher_descs pd ON (random() * 499 + 1)::int = pd.rn\n")
        f.write("JOIN temp_publisher_websites pw ON (random() * 499 + 1)::int = pw.rn\n")
        f.write("WHERE u.rn <= 5000;\n\n")
        
        # 5. Generar datos de usuarios
        f.write("-- ============ GENERACIÓN DE USUARIOS ============\n")
        f.write("-- TABLA TEMPORAL CON NOMBRES DE USUARIOS\n")
        f.write("CREATE TEMP TABLE temp_user_names AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    nombre_completo\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 100,000 nombres en bloques
        batch_size = 50000
        total_users = 100000
        
        for i in range(0, total_users, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_users:
                    break
                full_name = fake.unique.name()
                batch.append(f"        ('{full_name.replace("'", "''")}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_users:
                f.write(",\n")
        
        f.write("\n    ) AS names(nombre_completo);\n\n")
        
        # Insertar usuarios
        f.write("INSERT INTO public.\"user\" (\n")
        f.write("    user_id, \"password\", \"name\", profile_picture, is_premium, created_at, user_type\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_user,\n")
        f.write("    encode(gen_random_bytes(16), 'hex'),\n")
        f.write("    n.nombre_completo,\n")
        f.write("    NULL,\n")
        f.write("    CASE WHEN random() < 0.2 THEN true ELSE false END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '365 days'),\n")
        f.write("    CASE \n")
        f.write("        WHEN random() < 0.1 THEN 1 -- 10% admin\n")
        f.write("        WHEN random() < 0.3 THEN 2 -- 20% premium (del 10 al 30%)\n")
        f.write("        ELSE 3 -- 70% regular\n")
        f.write("    END\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("JOIN temp_user_names n ON u.rn = n.rn;\n\n")
        
        # 6. Generar suscripciones
        f.write("-- ============ GENERACIÓN DE SUSCRIPCIONES ============\n")
        f.write("INSERT INTO public.\"subscription\" (\n")
        f.write("    subscription_id, user_id, plan_type, start_date, end_date, payment_status\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_subscription,\n")
        f.write("    u.id_user,\n")
        f.write("    (random() * 2 + 1)::int, -- plan_type entre 1 y 3\n")
        f.write("    CURRENT_DATE - (random() * interval '365 days'),\n")
        f.write("    CURRENT_DATE + (random() * interval '365 days'),\n")
        f.write("    CASE \n")
        f.write("        WHEN random() < 0.7 THEN 2 -- 70% Pagado\n")
        f.write("        WHEN random() < 0.85 THEN 1 -- 15% Pendiente\n")
        f.write("        WHEN random() < 0.95 THEN 3 -- 10% Cancelado\n")
        f.write("        ELSE 4 -- 5% Rechazado\n")
        f.write("    END\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("WHERE random() < 0.5; -- 50% de usuarios tienen suscripción\n\n")
        
        # 7. Generar datos de libros
        f.write("-- ============ GENERACIÓN DE LIBROS ============\n")
        f.write("-- TABLA TEMPORAL CON DATOS DE LIBROS\n")
        f.write("CREATE TEMP TABLE temp_book_data AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    titulo,\n")
        f.write("    sinopsis,\n")
        f.write("    idioma,\n")
        f.write("    CASE WHEN random() < 0.3 THEN true ELSE false END AS es_audiolibro -- 30% audiolibros\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Lista de idiomas posibles
        idiomas = ['es', 'en', 'fr', 'de', 'it', 'pt']
        
        # Generar 100,000 libros en bloques
        for i in range(0, total_users, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_users:
                    break
                titulo = fake.catch_phrase()[:40].replace("'", "''")
                sinopsis = fake.paragraph(nb_sentences=3).replace("'", "''")
                idioma = random.choice(idiomas)
                
                batch.append(f"        ('{titulo}', '{sinopsis}', '{idioma}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_users:
                f.write(",\n")
        
        f.write("\n    ) AS books(titulo, sinopsis, idioma);\n\n")
        
        # Insertar libros con relaciones correctas
        f.write("INSERT INTO public.\"book\" (\n")
        f.write("    book_id, title, author, synopsis, cover_image, language, is_audiobook, file_url,\n")
        f.write("    created_at, updated_at, uploaded_by, publisher_id, published_year, isbn\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_book,\n")
        f.write("    b.titulo,\n")
        f.write("    a.author_id,  -- Usar el ID de autor existente\n")
        f.write("    b.sinopsis,\n")
        f.write("    NULL,\n")
        f.write("    b.idioma,\n")
        f.write("    b.es_audiolibro,\n")
        f.write("    '/books/' || replace(lower(b.titulo), ' ', '_') || CASE WHEN b.es_audiolibro THEN '.mp3' ELSE '.pdf' END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '365 days'),\n")
        f.write("    NULL,\n")
        f.write("    (SELECT user_id FROM public.\"user\" WHERE user_type = 1 ORDER BY random() LIMIT 1),\n")
        f.write("    CASE WHEN random() < 0.8 THEN (SELECT publisher_id FROM public.\"publisher\" ORDER BY random() LIMIT 1) ELSE NULL END,\n")
        f.write("    (CURRENT_DATE - (random() * interval '50 years'))::date,\n")
        f.write("    CASE WHEN random() < 0.7 THEN NULL ELSE substring(md5(random()::text), 1, 13) END\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("JOIN temp_book_data b ON u.rn = b.rn\n")
        f.write("JOIN public.\"author\" a ON true  -- Garantiza que haya un autor existente\n")
        f.write("ORDER BY random() LIMIT 100000;\n")
        
        # 8. Generar datos de audiolibros (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE AUDIOLIBROS ============\n")
        f.write("-- Primero creamos una tabla temporal con los narradores\n")
        f.write("CREATE TEMP TABLE temp_narrators AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    narrator\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 500 nombres de narradores
        batch_size = 100
        total_narrators = 500
        
        for i in range(0, total_narrators, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_narrators:
                    break
                narrator = fake.name().replace("'", "''")
                batch.append(f"        ('{narrator}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_narrators:
                f.write(",\n")
        
        f.write("\n    ) AS narrators(narrator);\n\n")
        
        f.write("INSERT INTO public.\"audiobook\" (\n")
        f.write("    book_id, duration, narrator, audio_file_url\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    b.book_id,\n")
        f.write("    (60 + random() * 540)::int, -- Duración entre 1 y 10 horas\n")
        f.write("    n.narrator,\n")
        f.write("    '/audiobooks/' || replace(lower(b.title), ' ', '_') || '.mp3'\n")
        f.write("FROM public.\"book\" b\n")
        f.write("JOIN temp_narrators n ON (random() * 499 + 1)::int = n.rn\n")
        f.write("WHERE b.is_audiobook = true;\n\n")
        
        # 9. Generar reseñas (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE RESEÑAS ============\n")
        f.write("-- Tabla temporal con comentarios para reseñas\n")
        f.write("CREATE TEMP TABLE temp_review_comments AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    comment\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 1000 comentarios de reseña
        total_comments = 1000
        
        for i in range(0, total_comments, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_comments:
                    break
                comment = fake.sentence(nb_words=10).replace("'", "''")
                batch.append(f"        ('{comment}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_comments:
                f.write(",\n")
        
        f.write("\n    ) AS comments(comment);\n\n")
        
        f.write("INSERT INTO public.\"review\" (\n")
        f.write("    review_id, rating, \"comment\", created_at, user_id, book_id\n")
        f.write(")\n")
        f.write("WITH libros_con_resenas AS (\n")
        f.write("    SELECT \n")
        f.write("        b.book_id,\n")
        f.write("        u.id_user,\n")
        f.write("        row_number() OVER (PARTITION BY b.book_id ORDER BY random()) as rn\n")
        f.write("    FROM public.\"book\" b\n")
        f.write("    CROSS JOIN (SELECT id_user FROM uuid_temp_entities ORDER BY random() LIMIT 100000) u\n")
        f.write("    WHERE random() < 0.4\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    gen_random_uuid(), -- Generar nuevo UUID para cada reseña\n")
        f.write("    (random() * 4 + 1)::int, -- rating entre 1 y 5\n")
        f.write("    CASE WHEN random() < 0.7 THEN (SELECT comment FROM temp_review_comments ORDER BY random() LIMIT 1) ELSE NULL END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '180 days'),\n")
        f.write("    id_user,\n")
        f.write("    book_id\n")
        f.write("FROM libros_con_resenas\n")
        f.write("WHERE rn <= 5; -- Máximo 5 reseñas por libro\n\n")        
        
        # 10. Generar favoritos
        f.write("-- ============ GENERACIÓN DE FAVORITOS ============\n")
        f.write("INSERT INTO public.\"favorite\" (\n")
        f.write("    favorite_id, created_at, user_id, book_id\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_favorite,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '90 days'),\n")
        f.write("    u.id_user,\n")
        f.write("    u.id_book\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("WHERE random() < 0.3; -- 30% de usuarios marcan libros como favoritos\n\n")
        
        # 11. Generar seguimientos (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE SEGUIMIENTOS ============\n")
        f.write("INSERT INTO public.\"follow\" (\n")
        f.write("    follow_id, created_at, follower_id, followed_id\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    gen_random_uuid(), -- Generar nuevo UUID para cada seguimiento\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '120 days'),\n")
        f.write("    u1.id_user,\n")
        f.write("    u2.id_user\n")
        f.write("FROM \n")
        f.write("    (SELECT id_user FROM uuid_temp_entities ORDER BY random() LIMIT 300000) u1\n")
        f.write("    CROSS JOIN LATERAL (\n")
        f.write("        SELECT id_user FROM uuid_temp_entities \n")
        f.write("        WHERE id_user != u1.id_user \n")
        f.write("        ORDER BY random() LIMIT 1\n")
        f.write("    ) u2\n")
        f.write("WHERE random() < 0.2;\n\n")
        
        # 12. Generar listas de lectura (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE LISTAS DE LECTURA ============\n")
        f.write("-- Tabla temporal con descripciones para listas\n")
        f.write("CREATE TEMP TABLE temp_list_descriptions AS\n")
        f.write("SELECT \n")
        f.write("    row_number() OVER () AS rn,\n")
        f.write("    description\n")
        f.write("FROM (\n")
        f.write("    VALUES\n")
        
        # Generar 500 descripciones
        total_descriptions = 500
        
        for i in range(0, total_descriptions, batch_size):
            batch = []
            for _ in range(batch_size):
                if i + _ >= total_descriptions:
                    break
                desc = fake.sentence(nb_words=6).replace("'", "''")
                batch.append(f"        ('{desc}')")
            
            f.write(",\n".join(batch))
            if i + batch_size < total_descriptions:
                f.write(",\n")
        
        f.write("\n    ) AS descriptions(description);\n\n")
        
        f.write("INSERT INTO public.\"reading_list\" (\n")
        f.write("    list_id, \"name\", description, created_by, is_public, created_at\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_reading_list,\n")
        f.write("    'Mi lista ' || substring(md5(random()::text), 1, 6),\n")
        f.write("    CASE \n")
        f.write("        WHEN random() < 0.6 THEN (SELECT description FROM temp_list_descriptions ORDER BY random() LIMIT 1)\n")
        f.write("        ELSE NULL\n")
        f.write("    END,\n")
        f.write("    u.id_user,\n")
        f.write("    CASE WHEN random() < 0.7 THEN true ELSE false END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '60 days')\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("WHERE random() < 0.25;\n\n")
        
        # 13. Generar items de listas de lectura (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE ITEMS EN LISTAS ============\n")
        f.write("INSERT INTO public.\"reading_list_item\" (\n")
        f.write("    list_id, book_id, added_at\n")
        f.write(")\n")
        f.write("WITH list_book_pairs AS (\n")
        f.write("    SELECT \n")
        f.write("        r.list_id,\n")
        f.write("        (SELECT book_id FROM public.\"book\" ORDER BY random() LIMIT 1) as book_id,\n")
        f.write("        r.created_at + (random() * interval '7 days') as added_at\n")
        f.write("    FROM public.\"reading_list\" r\n")
        f.write("    CROSS JOIN generate_series(1, (random() * 4 + 1)::int) -- 1-5 libros por lista\n")
        f.write(")\n")
        f.write("SELECT list_id, book_id, added_at FROM list_book_pairs;\n\n")
        
        # 14. Generar notificaciones (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE NOTIFICACIONES ============\n")
        f.write("INSERT INTO public.\"notification\" (\n")
        f.write("    notification_id, message, is_read, created_at, user_id, notification_type\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    gen_random_uuid(), -- Generar nuevo UUID para cada notificación\n")
        f.write("    CASE nt.notification_type_id\n")
        f.write("        WHEN 1 THEN 'Nuevo libro disponible: ' || substring(md5(random()::text), 1, 10)\n")
        f.write("        WHEN 2 THEN 'Recordatorio: Continúa leyendo ' || substring(md5(random()::text), 1, 10)\n")
        f.write("        WHEN 3 THEN 'Promoción especial: ' || substring(md5(random()::text), 1, 15)\n")
        f.write("        ELSE substring(md5(random()::text), 1, 10) || ' ha empezado a seguirte'\n")
        f.write("    END,\n")
        f.write("    CASE WHEN random() < 0.6 THEN true ELSE false END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '30 days'),\n")
        f.write("    u.id_user,\n")
        f.write("    nt.notification_type_id\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("CROSS JOIN (SELECT notification_type_id FROM public.\"notification_type\") nt\n")
        f.write("WHERE random() < 0.2;\n\n")
        
        # 15. Generar métricas de libros (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE MÉTRICAS DE LIBROS ============\n")
        f.write("INSERT INTO public.\"book_metrics\" (\n")
        f.write("    book_id, total_reads, total_listens, total_favorites, total_reviews, average_rating, last_read_at, updated_at\n")
        f.write(")\n")
        f.write("WITH review_stats AS (\n")
        f.write("    SELECT \n")
        f.write("        book_id, \n")
        f.write("        COUNT(*) as review_count,\n")
        f.write("        AVG(rating) as avg_rating\n")
        f.write("    FROM public.\"review\"\n")
        f.write("    GROUP BY book_id\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    b.book_id,\n")
        f.write("    (random() * 10000)::int,\n")
        f.write("    CASE WHEN b.is_audiobook THEN (random() * 5000)::int ELSE 0 END,\n")
        f.write("    (SELECT COUNT(*) FROM public.\"favorite\" f WHERE f.book_id = b.book_id),\n")
        f.write("    COALESCE(r.review_count, 0),\n")
        f.write("    CASE \n")
        f.write("        WHEN r.review_count > 0 THEN LEAST(GREATEST(r.avg_rating, 1.0), 5.0)\n")
        f.write("        ELSE 0\n")
        f.write("    END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '7 days'),\n")
        f.write("    CURRENT_TIMESTAMP\n")
        f.write("FROM public.\"book\" b\n")
        f.write("LEFT JOIN review_stats r ON b.book_id = r.book_id;\n\n")
        
        # 16. Generar promociones (CORREGIDO)
        f.write("-- ============ GENERACIÓN DE PROMOCIONES ============\n")
        f.write("INSERT INTO public.\"promotion\" (\n")
        f.write("    promotion_id, book_id, title, description, start_date, end_date, discount_percent, banner_image_url, created_at\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    gen_random_uuid(), -- Generar nuevo UUID para cada promoción\n")
        f.write("    b.book_id,\n")
        f.write("    'Promoción de ' || substring(b.title, 1, 20),\n")
        f.write("    'No te pierdas esta oferta especial en ' || b.title,\n")
        f.write("    CURRENT_DATE,\n")
        f.write("    CURRENT_DATE + (random() * interval '30 days'),\n")
        f.write("    (random() * 50 + 10)::int, -- Descuento entre 10% y 60%\n")
        f.write("    '/banners/' || substring(md5(random()::text), 1, 10) || '.jpg',\n")
        f.write("    CURRENT_TIMESTAMP\n")
        f.write("FROM \n")
        f.write("    (SELECT book_id, title FROM public.\"book\" ORDER BY random() LIMIT 10000) b;\n\n")
        
        # 17. Generar campañas publicitarias (ACTUALIZADO)
        f.write("-- ============ GENERACIÓN DE CAMPAÑAS PUBLICITARIAS ============\n")
        f.write("INSERT INTO public.\"ad_campaign\" (\n")
        f.write("    ad_id, title, image_url, target_url, book_id, created_by, \n")
        f.write("    visible_to_plan, start_date, end_date, impressions, clicks, created_at\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    gen_random_uuid(), -- Genera un UUID único para cada campaña\n")
        f.write("    'Descubre: ' || substring(b.title, 1, 15),\n")
        f.write("    '/ads/' || substring(md5(random()::text), 1, 10) || '.jpg',\n")
        f.write("    '/book/' || b.book_id,\n")
        f.write("    b.book_id,\n")
        f.write("    (SELECT user_id FROM public.\"user\" WHERE user_type = 1 ORDER BY random() LIMIT 1),\n")
        f.write("    (random() * 2 + 1)::int, -- plan_type entre 1 y 3\n")
        f.write("    CURRENT_DATE - (random() * interval '15 days'),\n")
        f.write("    CURRENT_DATE + (random() * interval '30 days'),\n")
        f.write("    (random() * 100000)::int,\n")
        f.write("    (random() * 1000)::int,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '20 days')\n")
        f.write("FROM \n")
        f.write("    (SELECT book_id, title FROM public.\"book\" ORDER BY random() LIMIT 5000) b;\n\n")
        
        # 18. Generar relación user_book
        f.write("-- ============ GENERACIÓN DE USER_BOOK ============\n")
        f.write("INSERT INTO public.\"user_book\" (\n")
        f.write("    user_id, book_id, pages_read, minutes_listened, last_accessed\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    u.id_user,\n")
        f.write("    u.id_book,\n")
        f.write("    CASE WHEN b.is_audiobook THEN 0 ELSE (random() * 500)::int END,\n")
        f.write("    CASE WHEN b.is_audiobook THEN (random() * COALESCE(ab.duration, 0))::int ELSE 0 END,\n")
        f.write("    CURRENT_TIMESTAMP - (random() * interval '30 days')\n")
        f.write("FROM uuid_temp_entities u\n")
        f.write("JOIN public.\"book\" b ON u.id_book = b.book_id\n")
        f.write("LEFT JOIN public.\"audiobook\" ab ON b.book_id = ab.book_id\n")
        f.write("WHERE random() < 0.7; -- 70% de usuarios tendrán al menos un libro\n\n")
        
        # 19. Generar géneros de libros
        f.write("-- ============ GENERACIÓN DE GÉNEROS DE LIBROS ============\n")
        f.write("INSERT INTO public.\"genre_book\" (\n")
        f.write("    book_id, genre_type_id\n")
        f.write(")\n")
        f.write("WITH libros_con_generos AS (\n")
        f.write("    SELECT \n")
        f.write("        b.book_id,\n")
        f.write("        gt.genre_type_id,\n")
        f.write("        row_number() OVER (PARTITION BY b.book_id ORDER BY random()) as rn\n")
        f.write("    FROM \n")
        f.write("        public.\"book\" b\n")
        f.write("    CROSS JOIN \n")
        f.write("        public.\"genre_type\" gt\n")
        f.write("    WHERE random() < 0.7 -- 70% de probabilidad de asignar género\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    book_id,\n")
        f.write("    genre_type_id\n")
        f.write("FROM \n")
        f.write("    libros_con_generos\n")
        f.write("WHERE \n")
        f.write("    rn <= 3; -- Máximo 3 géneros por libro\n\n")
        
        # 20. Generar etiquetas de libros
        f.write("-- ============ GENERACIÓN DE ETIQUETAS DE LIBROS ============\n")
        f.write("INSERT INTO public.\"book_tag\" (\n")
        f.write("    book_id, tag_id\n")
        f.write(")\n")
        f.write("WITH libros_con_etiquetas AS (\n")
        f.write("    SELECT \n")
        f.write("        b.book_id,\n")
        f.write("        t.tag_id,\n")
        f.write("        row_number() OVER (PARTITION BY b.book_id ORDER BY random()) as rn\n")
        f.write("    FROM \n")
        f.write("        public.\"book\" b\n")
        f.write("    CROSS JOIN \n")
        f.write("        public.\"tag\" t\n")
        f.write("    WHERE random() < 0.5 -- 50% de probabilidad de asignar etiqueta\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    book_id,\n")
        f.write("    tag_id\n")
        f.write("FROM \n")
        f.write("    libros_con_etiquetas\n")
        f.write("WHERE \n")
        f.write("    rn <= 2; -- Máximo 2 etiquetas por libro\n\n")

        # 21. Generar similitud entre libros (NUEVO)
        f.write("-- ============ GENERACIÓN DE SIMILITUD ENTRE LIBROS ============\n")
        f.write("INSERT INTO public.\"book_similarity\" (\n")
        f.write("    book_id_1, book_id_2, similarity_score\n")
        f.write(")\n")
        f.write("WITH pares_libros AS (\n")
        f.write("    SELECT \n")
        f.write("        b1.book_id as book_id_1,\n")
        f.write("        b2.book_id as book_id_2\n")
        f.write("    FROM \n")
        f.write("        (SELECT book_id FROM public.\"book\" ORDER BY random() LIMIT 10000) b1\n")
        f.write("    CROSS JOIN \n")
        f.write("        (SELECT book_id FROM public.\"book\" ORDER BY random() LIMIT 10000) b2\n")
        f.write("    WHERE \n")
        f.write("        b1.book_id != b2.book_id\n")
        f.write("        AND random() < 0.1 -- 10% de probabilidad de crear relación\n")
        f.write(")\n")
        f.write("SELECT \n")
        f.write("    book_id_1,\n")
        f.write("    book_id_2,\n")
        f.write("    (random() * 0.9 + 0.1)::numeric(3,2) -- Score entre 0.1 y 1.0\n")
        f.write("FROM \n")
        f.write("    pares_libros\n")
        f.write("LIMIT 5000; -- Limitar a 50,000 relaciones de similitud\n\n")
        
        # Mensaje final y limpieza
        f.write("-- Limpieza de tablas temporales\n")
        f.write("DROP TABLE IF EXISTS uuid_temp_entities;\n")
        f.write("DROP TABLE IF EXISTS temp_user_names;\n")
        f.write("DROP TABLE IF EXISTS temp_book_data;\n\n")

if __name__ == "__main__":
    print("Generando archivo SQL con datos completos y todas las relaciones...")
    generate_sql_file()
    print("Archivo 'generate_data_corrected.sql' generado exitosamente!")