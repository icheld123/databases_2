-- 1. Insertar datos en tablas de tipos/catálogos
INSERT INTO "user_type" ("description") VALUES ('Administrador'), ('Usuario Premium'), ('Usuario Regular');

INSERT INTO "plan_type" ("description") VALUES ('Básico'), ('Premium'), ('Premium Plus');

INSERT INTO "payment_status_type" ("description") VALUES ('Pendiente'), ('Pagado'), ('Cancelado'), ('Rechazado');

INSERT INTO "notification_type" ("description") VALUES ('Nuevo libro'), ('Recordatorio'), ('Promoción'), ('Seguimiento');

INSERT INTO "genre_type" ("description") VALUES ('Ficción'), ('No ficción'), ('Misterio'), ('Romance'), ('Ciencia ficción'), ('Fantasía'), ('Biografía'), ('Historia');

INSERT INTO "tag" ("description") VALUES ('Bestseller'), ('Nuevo'), ('Recomendado'), ('Clásico'), ('Trending'), ('Award Winner');

-- 2. Insertar algunos países (usando los existentes en countries.sql)

-- 3. Insertar usuario principal
INSERT INTO "user" ("user_id", "password", "name", "is_premium", "user_type") 
VALUES ('01234567-89ab-cdef-0123-456789abcdef', 'password123', 'Ana García López', true, 2);

-- 4. Insertar autores
INSERT INTO "author" ("author_id", "name", "biography", "nationality") 
VALUES 
('11111111-1111-1111-1111-111111111111', 'Gabriel García Márquez', 'Escritor, novelista, cuentista, guionista, editor y periodista colombiano. Premio Nobel de Literatura en 1982.', 46),
('22222222-2222-2222-2222-222222222222', 'Isabel Allende', 'Escritora chilena nacionalizada estadounidense. Es considerada la novelista de lengua española más leída del mundo.', 42);

-- 5. Insertar editorial
INSERT INTO "publisher" ("publisher_id", "name", "country_id", "founded_year", "website", "description") 
VALUES ('33333333-3333-3333-3333-333333333333', 'Editorial Planeta', 46, 1949, 'https://www.planetadelibros.com', 'Una de las editoriales más importantes de España y América Latina.');

-- 6. Insertar libros
INSERT INTO "book" ("book_id", "title", "author", "synopsis", "language", "is_audiobook", "file_url", "uploaded_by", "publisher_id", "published_year", "isbn") 
VALUES 
('44444444-4444-4444-4444-444444444444', 'Cien años de soledad', '11111111-1111-1111-1111-111111111111', 'La novela narra la historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo.', 'Español', false, 'https://books.example.com/cien-anos-soledad.pdf', '01234567-89ab-cdef-0123-456789abcdef', '33333333-3333-3333-3333-333333333333', '1967-01-01', '978-84-376-0494-7'),
('55555555-5555-5555-5555-555555555555', 'La casa de los espíritus', '22222222-2222-2222-2222-222222222222', 'Primera novela de Isabel Allende, cuenta la historia de cuatro generaciones de una familia chilena.', 'Español', true, 'https://books.example.com/casa-espiritus.pdf', '01234567-89ab-cdef-0123-456789abcdef', '33333333-3333-3333-3333-333333333333', '1982-01-01', '978-84-204-6602-7');

-- 7. Insertar audiobook para uno de los libros
INSERT INTO "audiobook" ("book_id", "duration", "narrator", "audio_file_url") 
VALUES ('55555555-5555-5555-5555-555555555555', 720, 'María Fernanda Yepes', 'https://audio.example.com/casa-espiritus.mp3');

-- 8. Insertar métricas de libros
INSERT INTO "book_metrics" ("book_id", "total_reads", "total_listens", "total_favorites", "total_reviews", "average_rating", "last_read_at") 
VALUES 
('44444444-4444-4444-4444-444444444444', 1250, 0, 890, 234, 4.8, '2025-07-01 15:30:00'),
('55555555-5555-5555-5555-555555555555', 750, 450, 320, 156, 4.6, '2025-07-02 10:45:00');

-- 9. Insertar géneros para los libros
INSERT INTO "genre_book" ("book_id", "genre_type_id") 
VALUES 
('44444444-4444-4444-4444-444444444444', 1), -- Ficción
('44444444-4444-4444-4444-444444444444', 6), -- Fantasía
('55555555-5555-5555-5555-555555555555', 1), -- Ficción
('55555555-5555-5555-5555-555555555555', 8); -- Historia

-- 10. Insertar tags para los libros
INSERT INTO "book_tag" ("book_id", "tag_id") 
VALUES 
('44444444-4444-4444-4444-444444444444', 1), -- Bestseller
('44444444-4444-4444-4444-444444444444', 4), -- Clásico
('44444444-4444-4444-4444-444444444444', 6), -- Award Winner
('55555555-5555-5555-5555-555555555555', 1), -- Bestseller
('55555555-5555-5555-5555-555555555555', 3); -- Recomendado

-- 11. Insertar reseñas del usuario
INSERT INTO "review" ("review_id", "rating", "comment", "user_id", "book_id") 
VALUES 
('66666666-6666-6666-6666-666666666666', 5, 'Una obra maestra de la literatura latinoamericana. Imprescindible.', '01234567-89ab-cdef-0123-456789abcdef', '44444444-4444-4444-4444-444444444444'),
('77777777-7777-7777-7777-777777777777', 4, 'Excelente narración, muy emotiva. El audiolibro es fantástico.', '01234567-89ab-cdef-0123-456789abcdef', '55555555-5555-5555-5555-555555555555');

-- 12. Agregar libros a favoritos
INSERT INTO "favorite" ("favorite_id", "user_id", "book_id") 
VALUES 
('88888888-8888-8888-8888-888888888888', '01234567-89ab-cdef-0123-456789abcdef', '44444444-4444-4444-4444-444444444444'),
('99999999-9999-9999-9999-999999999999', '01234567-89ab-cdef-0123-456789abcdef', '55555555-5555-5555-5555-555555555555');

-- 13. Insertar progreso de lectura
INSERT INTO "user_book" ("user_id", "book_id", "pages_read", "minutes_listened", "last_accessed") 
VALUES 
('01234567-89ab-cdef-0123-456789abcdef', '44444444-4444-4444-4444-444444444444', 350, 0, '2025-07-03 20:15:00'),
('01234567-89ab-cdef-0123-456789abcdef', '55555555-5555-5555-5555-555555555555', 0, 120, '2025-07-04 09:30:00');

-- 14. Crear lista de lectura
INSERT INTO "reading_list" ("list_id", "name", "description", "created_by", "is_public") 
VALUES ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Mis Clásicos Favoritos', 'Una colección de libros clásicos que todo el mundo debería leer', '01234567-89ab-cdef-0123-456789abcdef', true);

-- 15. Agregar libros a la lista de lectura
INSERT INTO "reading_list_item" ("list_id", "book_id") 
VALUES 
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '44444444-4444-4444-4444-444444444444'),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '55555555-5555-5555-5555-555555555555');

-- 16. Insertar suscripción del usuario
INSERT INTO "subscription" ("subscription_id", "user_id", "plan_type", "start_date", "end_date", "payment_status") 
VALUES ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '01234567-89ab-cdef-0123-456789abcdef', 2, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 2);

-- 17. Insertar notificaciones para el usuario
INSERT INTO "notification" ("notification_id", "message", "is_read", "user_id", "notification_type") 
VALUES 
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Nuevo libro disponible en tu género favorito', false, '01234567-89ab-cdef-0123-456789abcdef', 1),
('dddddddd-dddd-dddd-dddd-dddddddddddd', 'Recordatorio: continúa leyendo', true, '01234567-89ab-cdef-0123-456789abcdef', 2);

-- 18. Insertar métricas del usuario
INSERT INTO "user_metrics" ("user_id", "books_read", "minutes_listened", "reviews_written", "favorites_count", "total_pages_read", "active_days", "last_active_at") 
VALUES ('01234567-89ab-cdef-0123-456789abcdef', 2, 120, 2, 2, 350, 45, '2025-07-04 09:30:00');

-- 19. Insertar similitud entre libros
INSERT INTO "book_similarity" ("book_id_1", "book_id_2", "similarity_score") 
VALUES ('44444444-4444-4444-4444-444444444444', '55555555-5555-5555-5555-555555555555', 0.75);

-- 20. Insertar promoción para uno de los libros
INSERT INTO "promotion" ("promotion_id", "book_id", "title", "description", "start_date", "end_date", "discount_percent", "banner_image_url") 
VALUES ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '55555555-5555-5555-5555-555555555555', 'Descuento Especial - Literatura Latinoamericana', 'Disfruta de un 20% de descuento en este clásico de Isabel Allende', '2025-07-01 00:00:00', '2025-07-31 23:59:59', 20, 'https://images.example.com/promo-casa-espiritus.jpg');

-- 21. Insertar campaña publicitaria
INSERT INTO "ad_campaign" ("ad_id", "title", "image_url", "target_url", "book_id", "created_by", "visible_to_plan", "start_date", "end_date", "impressions", "clicks") 
VALUES ('ffffffff-ffff-ffff-ffff-ffffffffffff', 'Descubre los Clásicos', 'https://images.example.com/ad-clasicos.jpg', 'https://bookmate.com/clasicos', '44444444-4444-4444-4444-444444444444', '01234567-89ab-cdef-0123-456789abcdef', 1, '2025-07-01 00:00:00', '2025-07-31 23:59:59', 15000, 450);

