-- EKSTENSI UNTUK UUID (JIKA BELUM ADA)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =================================================================
-- TABEL INTI MOBIL
-- =================================================================

-- 1. Tabel Model Dasar Mobil
-- Menyimpan informasi umum tentang sebuah model (e.g., Avanza, Innova).
CREATE TABLE public.cars (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(100) NOT NULL UNIQUE,
    segment VARCHAR(50) -- e.g., 'Low MPV', 'Medium SUV', 'Sedan'
);
COMMENT ON TABLE public.cars IS 'Menyimpan model dasar mobil seperti Avanza, Innova, Rush.';

-- 2. Tabel Varian Spesifik Mobil
-- Tabel utama yang berisi detail setiap varian. Ini akan menjadi tabel terbesar.
CREATE TABLE public.car_variants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    car_id UUID REFERENCES public.cars(id) ON DELETE CASCADE,
    variant_name VARCHAR(150) NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    image_url TEXT,
    engine_spec VARCHAR(255), -- e.g., '1.5L 2NR-VE, 4 Cylinder, DOHC, Dual VVT-i'
    transmission VARCHAR(50), -- e.g., 'CVT', 'Manual'
    seating_capacity INT,
    fuel_type VARCHAR(50), -- e.g., 'Gasoline', 'Hybrid', 'Diesel'
    target_demographic VARCHAR(50), -- 'Gen Z', 'Millennial', 'Family', 'Executive'
    use_case TEXT, -- Keywords: 'Daily', 'Off-road', 'Business', 'Travel'
    benefits_summary TEXT, -- Paragraf singkat tentang keuntungan utama
    circumstances_summary TEXT, -- Kondisi ideal penggunaan mobil
    top_features JSONB -- e.g., '{"feature1": "TSS", "feature2": "9-inch Display"}'
);
COMMENT ON TABLE public.car_variants IS 'Detail spesifik untuk setiap varian, termasuk harga, spesifikasi, dan target pasar.';

-- =================================================================
-- TABEL PENDUKUNG  
-- =================================================================

-- 3. Tabel Aksesoris
-- Daftar aksesoris resmi yang tersedia.
CREATE TABLE public.accessories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(12, 2) NOT NULL
);
COMMENT ON TABLE public.accessories IS 'Daftar aksesoris resmi yang dapat dibeli.';

-- 4. Tabel Relasi Varian & Aksesoris (Many-to-Many)
-- Menghubungkan aksesoris mana yang cocok untuk varian mobil mana.
CREATE TABLE public.variant_accessories (
    variant_id UUID REFERENCES public.car_variants(id) ON DELETE CASCADE,
    accessory_id UUID REFERENCES public.accessories(id) ON DELETE CASCADE,
    PRIMARY KEY (variant_id, accessory_id)
);
COMMENT ON TABLE public.variant_accessories IS 'Tabel penghubung antara varian mobil dan aksesoris yang kompatibel.';

-- 5. Tabel Promosi
-- Menyimpan informasi promo yang aktif untuk varian tertentu.
CREATE TABLE public.promotions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    variant_id UUID REFERENCES public.car_variants(id) ON DELETE CASCADE,
    promo_title VARCHAR(255) NOT NULL,
    discount_amount DECIMAL(15, 2),
    discount_percentage DECIMAL(5, 2),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    terms_conditions TEXT
);
COMMENT ON TABLE public.promotions IS 'Informasi promo dan diskon aktif untuk varian mobil tertentu.';

-- 6. Tabel Stok & Inden
-- Informasi ketersediaan unit per wilayah/kota.
CREATE TABLE public.stock_inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    variant_id UUID REFERENCES public.car_variants(id) ON DELETE CASCADE,
    city VARCHAR(100) NOT NULL,
    stock_quantity INT NOT NULL,
    indent_estimate_weeks INT, -- Estimasi inden dalam minggu, NULL jika ready stock
    UNIQUE(variant_id, city)
);
COMMENT ON TABLE public.stock_inventory IS 'Informasi stok dan estimasi inden per kota.';

-- =================================================================
-- TABEL PENGETAHUAN (TERSTRUKTUR)
-- =================================================================

-- 7. Tabel Bengkel Modifikasi Rekomendasi
CREATE TABLE public.workshops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address TEXT,
    specialization TEXT -- e.g., 'Body Kit, Audio, Engine'
);
COMMENT ON TABLE public.workshops IS 'Daftar bengkel modifikasi yang direkomendasikan per kota.';

-- 8. Tabel Komunitas Resmi
CREATE TABLE public.communities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    base_city VARCHAR(100) NOT NULL,
    focus_model VARCHAR(100),
    contact_person VARCHAR(100)
);
COMMENT ON TABLE public.communities IS 'Daftar komunitas mobil resmi per kota.';

-- 9. Standar Pakaian Staf
CREATE TABLE public.dress_codes (
    id SERIAL PRIMARY KEY,
    role VARCHAR(100) NOT NULL, -- 'Salesman', 'Sales Counter', 'Kasir'
    day_of_week VARCHAR(20) NOT NULL, -- 'Senin-Kamis', 'Jumat', 'Sabtu'
    attire_description TEXT NOT NULL
);
COMMENT ON TABLE public.dress_codes IS 'Panduan standar pakaian untuk staf berdasarkan peran dan hari.';

-- =================================================================
-- DATA SEED - CARS
-- =================================================================

INSERT INTO public.cars (id, model_name, segment) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'Avanza', 'Low MPV'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Veloz', 'Low MPV'),
    ('550e8400-e29b-41d4-a716-446655440003', 'Innova', 'Medium MPV'),
    ('550e8400-e29b-41d4-a716-446655440004', 'Innova Zenix', 'Medium MPV'),
    ('550e8400-e29b-41d4-a716-446655440005', 'Rush', 'Compact SUV'),
    ('550e8400-e29b-41d4-a716-446655440006', 'Fortuner', 'Medium SUV'),
    ('550e8400-e29b-41d4-a716-446655440007', 'Hilux', 'Pickup Truck'),
    ('550e8400-e29b-41d4-a716-446655440008', 'Alphard', 'Premium MPV'),
    ('550e8400-e29b-41d4-a716-446655440009', 'Vellfire', 'Premium MPV'),
    ('550e8400-e29b-41d4-a716-446655440010', 'Camry', 'Executive Sedan');

-- =================================================================
-- DATA SEED - CAR VARIANTS
-- =================================================================

-- Avanza Variants
INSERT INTO public.car_variants (id, car_id, variant_name, price, image_url, engine_spec, transmission, seating_capacity, fuel_type, target_demographic, use_case, benefits_summary, circumstances_summary, top_features) VALUES
    ('650e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'Avanza 1.3 E MT', 230000000.00, 'https://example.com/avanza-e-mt.jpg', '1.3L Dual VVT-i, 4 Cylinder, DOHC', 'Manual', 7, 'Gasoline', 'Family', 'Daily, Travel', 'Mobil keluarga terjangkau dengan kapasitas 7 penumpang, irit bahan bakar, dan perawatan mudah', 'Cocok untuk keluarga muda yang membutuhkan kendaraan sehari-hari dengan budget terbatas', '{"feature1": "7 Seater", "feature2": "Fuel Efficient", "feature3": "Easy Maintenance"}'),
    ('650e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', 'Avanza 1.3 E CVT', 245000000.00, 'https://example.com/avanza-e-cvt.jpg', '1.3L Dual VVT-i, 4 Cylinder, DOHC', 'CVT', 7, 'Gasoline', 'Family', 'Daily, Travel', 'Mobil keluarga dengan transmisi otomatis yang nyaman dikendarai di macet', 'Ideal untuk keluarga yang sering berkendara di kota dengan kondisi lalu lintas padat', '{"feature1": "CVT Transmission", "feature2": "Smooth Driving", "feature3": "City Friendly"}'),
    ('650e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440001', 'Avanza 1.3 G CVT', 260000000.00, 'https://example.com/avanza-g-cvt.jpg', '1.3L Dual VVT-i, 4 Cylinder, DOHC', 'CVT', 7, 'Gasoline', 'Family', 'Daily, Travel', 'Varian tertinggi Avanza dengan fitur lengkap dan kenyamanan optimal', 'Cocok untuk keluarga yang menginginkan fitur lengkap dengan harga terjangkau', '{"feature1": "Premium Interior", "feature2": "Advanced Features", "feature3": "Complete Package"}');

-- Veloz Variants  
INSERT INTO public.car_variants (id, car_id, variant_name, price, image_url, engine_spec, transmission, seating_capacity, fuel_type, target_demographic, use_case, benefits_summary, circumstances_summary, top_features) VALUES
    ('650e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', 'Veloz 1.5 G CVT', 285000000.00, 'https://example.com/veloz-g-cvt.jpg', '1.5L Dual VVT-i, 4 Cylinder, DOHC', 'CVT', 7, 'Gasoline', 'Millennial', 'Daily, Travel', 'MPV sporty dengan performa mesin 1.5L yang bertenaga dan desain yang stylish', 'Cocok untuk generasi milenial yang menginginkan MPV dengan tampilan sporty', '{"feature1": "Sporty Design", "feature2": "1.5L Engine", "feature3": "Modern Features"}'),
    ('650e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440002', 'Veloz 1.5 Q CVT TSS', 305000000.00, 'https://example.com/veloz-q-cvt-tss.jpg', '1.5L Dual VVT-i, 4 Cylinder, DOHC', 'CVT', 7, 'Gasoline', 'Millennial', 'Daily, Travel', 'Varian tertinggi Veloz dengan Toyota Safety Sense dan fitur premium', 'Ideal untuk yang mengutamakan keselamatan dan teknologi terdepan', '{"feature1": "Toyota Safety Sense", "feature2": "Premium Package", "feature3": "Advanced Safety"}');

-- Innova Variants
INSERT INTO public.car_variants (id, car_id, variant_name, price, image_url, engine_spec, transmission, seating_capacity, fuel_type, target_demographic, use_case, benefits_summary, circumstances_summary, top_features) VALUES
    ('650e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440003', 'Innova 2.0 G MT', 385000000.00, 'https://example.com/innova-g-mt.jpg', '2.0L Dual VVT-i, 4 Cylinder, DOHC', 'Manual', 8, 'Gasoline', 'Family', 'Daily, Travel, Business', 'MPV premium dengan kabin luas dan kenyamanan tinggi untuk keluarga besar', 'Cocok untuk keluarga besar atau bisnis yang membutuhkan kendaraan dengan kapasitas besar', '{"feature1": "8 Seater", "feature2": "Spacious Cabin", "feature3": "Premium Comfort"}'),
    ('650e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440003', 'Innova 2.0 G AT', 400000000.00, 'https://example.com/innova-g-at.jpg', '2.0L Dual VVT-i, 4 Cylinder, DOHC', 'Automatic', 8, 'Gasoline', 'Family', 'Daily, Travel, Business', 'Innova dengan transmisi otomatis untuk kenyamanan berkendara maksimal', 'Ideal untuk penggunaan bisnis atau keluarga yang sering melakukan perjalanan jauh', '{"feature1": "Automatic Transmission", "feature2": "Business Ready", "feature3": "Long Distance Comfort"}');

-- Innova Zenix Variants
INSERT INTO public.car_variants (id, car_id, variant_name, price, image_url, engine_spec, transmission, seating_capacity, fuel_type, target_demographic, use_case, benefits_summary, circumstances_summary, top_features) VALUES
    ('650e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440004', 'Innova Zenix 2.0 G CVT', 450000000.00, 'https://example.com/zenix-g-cvt.jpg', '2.0L Dynamic Force Engine, 4 Cylinder, DOHC', 'CVT', 7, 'Gasoline', 'Executive', 'Daily, Business, Travel', 'MPV premium terbaru dengan teknologi hibrid dan desain modern', 'Cocok untuk eksekutif muda yang menginginkan MPV dengan teknologi terdepan', '{"feature1": "Hybrid Technology", "feature2": "Modern Design", "feature3": "Executive Class"}'),
    ('650e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440004', 'Innova Zenix 2.0 V CVT HEV', 520000000.00, 'https://example.com/zenix-v-hev.jpg', '2.0L Dynamic Force Engine + Hybrid, 4 Cylinder, DOHC', 'CVT', 7, 'Hybrid', 'Executive', 'Daily, Business, Travel', 'Varian hybrid tertinggi dengan efisiensi bahan bakar terbaik', 'Ideal untuk yang mengutamakan efisiensi bahan bakar dan ramah lingkungan', '{"feature1": "Full Hybrid", "feature2": "Fuel Efficient", "feature3": "Eco Friendly"}');

-- Rush Variants
INSERT INTO public.car_variants (id, car_id, variant_name, price, image_url, engine_spec, transmission, seating_capacity, fuel_type, target_demographic, use_case, benefits_summary, circumstances_summary, top_features) VALUES
    ('650e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440005', 'Rush 1.5 G MT', 290000000.00, 'https://example.com/rush-g-mt.jpg', '1.5L Dual VVT-i, 4 Cylinder, DOHC', 'Manual', 7, 'Gasoline', 'Gen Z', 'Daily, Off-road', 'SUV kompak dengan ground clearance tinggi, cocok untuk berbagai medan', 'Cocok untuk anak muda yang suka petualangan dan berkendara di berbagai medan', '{"feature1": "High Ground Clearance", "feature2": "Adventure Ready", "feature3": "Compact SUV"}'),
    ('650e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440005', 'Rush 1.5 G AT', 305000000.00, 'https://example.com/rush-g-at.jpg', '1.5L Dual VVT-i, 4 Cylinder, DOHC', 'Automatic', 7, 'Gasoline', 'Gen Z', 'Daily, Off-road', 'Rush dengan transmisi otomatis untuk kemudahan berkendara di segala kondisi', 'Ideal untuk yang menginginkan SUV dengan kemudahan transmisi otomatis', '{"feature1": "Automatic Ease", "feature2": "Urban Adventure", "feature3": "Versatile Use"}');

-- Fortuner Variants
INSERT INTO public.car_variants (id, car_id, variant_name, price, image_url, engine_spec, transmission, seating_capacity, fuel_type, target_demographic, use_case, benefits_summary, circumstances_summary, top_features) VALUES
    ('650e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440006', 'Fortuner 2.4 G MT 4x2', 580000000.00, 'https://example.com/fortuner-g-mt.jpg', '2.4L D-4D Diesel, 4 Cylinder, DOHC, Turbo', 'Manual', 7, 'Diesel', 'Executive', 'Business, Off-road, Travel', 'SUV premium dengan mesin diesel bertenaga dan tampilan tangguh', 'Cocok untuk eksekutif yang membutuhkan kendaraan tangguh dan prestisius', '{"feature1": "Diesel Power", "feature2": "Premium SUV", "feature3": "Executive Status"}'),
    ('650e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-446655440006', 'Fortuner 2.8 VRZ AT 4x4', 750000000.00, 'https://example.com/fortuner-vrz-4x4.jpg', '2.8L D-4D Diesel, 4 Cylinder, DOHC, Turbo', 'Automatic', 7, 'Diesel', 'Executive', 'Business, Off-road, Travel', 'Varian tertinggi dengan sistem 4WD untuk petualangan ekstrem', 'Ideal untuk yang sering melakukan perjalanan off-road atau kondisi medan berat', '{"feature1": "4x4 System", "feature2": "Off-road Master", "feature3": "Ultimate Adventure"}');

-- =================================================================
-- DATA SEED - ACCESSORIES
-- =================================================================

INSERT INTO public.accessories (id, name, description, price) VALUES
    ('750e8400-e29b-41d4-a716-446655440001', 'Body Kit Sporty', 'Paket body kit untuk tampilan lebih sporty dan aerodinamis', 15000000.00),
    ('750e8400-e29b-41d4-a716-446655440002', 'Audio System Premium', 'Sistem audio premium dengan subwoofer dan speaker berkualitas tinggi', 25000000.00),
    ('750e8400-e29b-41d4-a716-446655440003', 'Roof Rack', 'Rak atap untuk membawa barang tambahan saat traveling', 3500000.00),
    ('750e8400-e29b-41d4-a716-446655440004', 'Mud Guard Set', 'Set mud guard untuk melindungi body dari cipratan lumpur', 1200000.00),
    ('750e8400-e29b-41d4-a716-446655440005', 'Dashboard Camera', 'Kamera dashboard untuk keamanan dan dokumentasi perjalanan', 2500000.00),
    ('750e8400-e29b-41d4-a716-446655440006', 'Window Film Premium', 'Kaca film premium untuk perlindungan dari sinar UV', 4000000.00),
    ('750e8400-e29b-41d4-a716-446655440007', 'Floor Mat Set', 'Set karpet lantai khusus untuk melindungi interior', 800000.00),
    ('750e8400-e29b-41d4-a716-446655440008', 'Side Visor', 'Talang air samping untuk kenyamanan saat hujan', 600000.00),
    ('750e8400-e29b-41d4-a716-446655440009', 'LED Headlight Upgrade', 'Upgrade lampu depan ke teknologi LED', 8000000.00),
    ('750e8400-e29b-41d4-a716-446655440010', 'Seat Cover Premium', 'Sarung jok premium untuk melindungi dan mempercantik interior', 3000000.00);

-- =================================================================
-- DATA SEED - VARIANT ACCESSORIES (Sample Associations)
-- =================================================================

-- Avanza accessories
INSERT INTO public.variant_accessories (variant_id, accessory_id) VALUES
    ('650e8400-e29b-41d4-a716-446655440001', '750e8400-e29b-41d4-a716-446655440004'),
    ('650e8400-e29b-41d4-a716-446655440001', '750e8400-e29b-41d4-a716-446655440005'),
    ('650e8400-e29b-41d4-a716-446655440001', '750e8400-e29b-41d4-a716-446655440006'),
    ('650e8400-e29b-41d4-a716-446655440001', '750e8400-e29b-41d4-a716-446655440007'),
    ('650e8400-e29b-41d4-a716-446655440001', '750e8400-e29b-41d4-a716-446655440008'),
    ('650e8400-e29b-41d4-a716-446655440001', '750e8400-e29b-41d4-a716-446655440010');

-- Veloz accessories
INSERT INTO public.variant_accessories (variant_id, accessory_id) VALUES
    ('650e8400-e29b-41d4-a716-446655440004', '750e8400-e29b-41d4-a716-446655440001'),
    ('650e8400-e29b-41d4-a716-446655440004', '750e8400-e29b-41d4-a716-446655440002'),
    ('650e8400-e29b-41d4-a716-446655440004', '750e8400-e29b-41d4-a716-446655440005'),
    ('650e8400-e29b-41d4-a716-446655440004', '750e8400-e29b-41d4-a716-446655440006'),
    ('650e8400-e29b-41d4-a716-446655440004', '750e8400-e29b-41d4-a716-446655440009'),
    ('650e8400-e29b-41d4-a716-446655440004', '750e8400-e29b-41d4-a716-446655440010');

-- Rush accessories  
INSERT INTO public.variant_accessories (variant_id, accessory_id) VALUES
    ('650e8400-e29b-41d4-a716-446655440010', '750e8400-e29b-41d4-a716-446655440001'),
    ('650e8400-e29b-41d4-a716-446655440010', '750e8400-e29b-41d4-a716-446655440003'),
    ('650e8400-e29b-41d4-a716-446655440010', '750e8400-e29b-41d4-a716-446655440004'),
    ('650e8400-e29b-41d4-a716-446655440010', '750e8400-e29b-41d4-a716-446655440005'),
    ('650e8400-e29b-41d4-a716-446655440010', '750e8400-e29b-41d4-a716-446655440009');

-- =================================================================
-- DATA SEED - PROMOTIONS
-- =================================================================

INSERT INTO public.promotions (id, variant_id, promo_title, discount_amount, discount_percentage, start_date, end_date, terms_conditions) VALUES
    ('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440001', 'Promo Akhir Tahun Avanza', 15000000.00, 0, '2024-12-01', '2024-12-31', 'Berlaku untuk pembelian tunai atau kredit. Tidak dapat digabung dengan promo lain.'),
    ('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440004', 'Veloz Special Discount', 0, 8.5, '2024-11-15', '2024-12-15', 'Khusus untuk pembelian kredit dengan DP minimum 25%. Termasuk asuransi comprehensive.'),
    ('850e8400-e29b-41d4-a716-446655440003', '650e8400-e29b-41d4-a716-446655440010', 'Rush Adventure Package', 20000000.00, 0, '2024-11-01', '2024-11-30', 'Paket termasuk aksesoris off-road senilai 10 juta. Berlaku untuk semua varian Rush.'),
    ('850e8400-e29b-41d4-a716-446655440004', '650e8400-e29b-41d4-a716-446655440008', 'Zenix Early Bird', 0, 5.0, '2024-10-01', '2024-12-31', 'Promo khusus peluncuran Innova Zenix. Termasuk extended warranty 5 tahun.');

-- =================================================================
-- DATA SEED - STOCK INVENTORY
-- =================================================================

INSERT INTO public.stock_inventory (id, variant_id, city, stock_quantity, indent_estimate_weeks) VALUES
    -- Jakarta
    ('950e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440001', 'Jakarta', 25, NULL),
    ('950e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440002', 'Jakarta', 15, NULL),
    ('950e8400-e29b-41d4-a716-446655440003', '650e8400-e29b-41d4-a716-446655440003', 'Jakarta', 8, NULL),
    ('950e8400-e29b-41d4-a716-446655440004', '650e8400-e29b-41d4-a716-446655440004', 'Jakarta', 12, NULL),
    ('950e8400-e29b-41d4-a716-446655440005', '650e8400-e29b-41d4-a716-446655440005', 'Jakarta', 0, 4),
    
    -- Surabaya
    ('950e8400-e29b-41d4-a716-446655440006', '650e8400-e29b-41d4-a716-446655440001', 'Surabaya', 18, NULL),
    ('950e8400-e29b-41d4-a716-446655440007', '650e8400-e29b-41d4-a716-446655440002', 'Surabaya', 10, NULL),
    ('950e8400-e29b-41d4-a716-446655440008', '650e8400-e29b-41d4-a716-446655440004', 'Surabaya', 5, NULL),
    ('950e8400-e29b-41d4-a716-446655440009', '650e8400-e29b-41d4-a716-446655440010', 'Surabaya', 8, NULL),
    
    -- Bandung
    ('950e8400-e29b-41d4-a716-446655440010', '650e8400-e29b-41d4-a716-446655440001', 'Bandung', 20, NULL),
    ('950e8400-e29b-41d4-a716-446655440011', '650e8400-e29b-41d4-a716-446655440003', 'Bandung', 0, 6),
    ('950e8400-e29b-41d4-a716-446655440012', '650e8400-e29b-41d4-a716-446655440006', 'Bandung', 3, NULL),
    
    -- Medan
    ('950e8400-e29b-41d4-a716-446655440013', '650e8400-e29b-41d4-a716-446655440001', 'Medan', 15, NULL),
    ('950e8400-e29b-41d4-a716-446655440014', '650e8400-e29b-41d4-a716-446655440004', 'Medan', 0, 8),
    ('950e8400-e29b-41d4-a716-446655440015', '650e8400-e29b-41d4-a716-446655440012', 'Medan', 2, NULL);

-- =================================================================
-- DATA SEED - WORKSHOPS
-- =================================================================

INSERT INTO public.workshops (id, name, city, address, specialization) VALUES
    ('a50e8400-e29b-41d4-a716-446655440001', 'AutoPro Modification', 'Jakarta', 'Jl. Gatot Subroto No. 123, Jakarta Selatan', 'Body Kit, Audio System, Engine Tuning'),
    ('a50e8400-e29b-41d4-a716-446655440002', 'Speed Garage', 'Jakarta', 'Jl. Sunter Permai Raya No. 45, Jakarta Utara', 'Performance Upgrade, Turbo Installation'),
    ('a50e8400-e29b-41d4-a716-446655440003', 'Custom Car Works', 'Surabaya', 'Jl. Ahmad Yani No. 78, Surabaya', 'Custom Interior, Audio, Lighting'),
    ('a50e8400-e29b-41d4-a716-446655440004', 'Modify Zone', 'Bandung', 'Jl. Dago No. 156, Bandung', 'Body Kit, Suspension, Exhaust System'),
    ('a50e8400-e29b-41d4-a716-446655440005', 'Turbo Garage', 'Medan', 'Jl. Sisingamangaraja No. 234, Medan', 'Engine Modification, Turbo, ECU Tuning');

-- =================================================================
-- DATA SEED - COMMUNITIES
-- =================================================================

INSERT INTO public.communities (id, name, base_city, focus_model, contact_person) VALUES
    ('b50e8400-e29b-41d4-a716-446655440001', 'Jakarta Avanza Club', 'Jakarta', 'Avanza', 'Budi Santoso - 081234567890'),
    ('b50e8400-e29b-41d4-a716-446655440002', 'Veloz Community Indonesia', 'Jakarta', 'Veloz', 'Andi Wijaya - 087654321098'),
    ('b50e8400-e29b-41d4-a716-446655440003', 'Innova Family Club', 'Surabaya', 'Innova', 'Sari Indrawati - 085678901234'),
    ('b50e8400-e29b-41d4-a716-446655440004', 'Rush Adventure Club', 'Bandung', 'Rush', 'Tommy Hermawan - 089012345678'),
    ('b50e8400-e29b-41d4-a716-446655440005', 'Toyota Fortuner Club', 'Medan', 'Fortuner', 'Rizki Pratama - 082345678901'),
    ('b50e8400-e29b-41d4-a716-446655440006', 'All Toyota Community', 'Jakarta', 'All Models', 'Maya Sari - 088765432109');

-- =================================================================
-- DATA SEED - DRESS CODES
-- =================================================================

INSERT INTO public.dress_codes (role, day_of_week, attire_description) VALUES
    ('Salesman', 'Senin-Kamis', 'Kemeja putih atau biru muda, celana kain hitam atau abu-abu, sepatu pantofel hitam, dasi opsional'),
    ('Salesman', 'Jumat', 'Kemeja batik atau kemeja polos dengan warna earth tone, celana kain, sepatu pantofel'),
    ('Salesman', 'Sabtu', 'Polo shirt berkerah dengan logo perusahaan, celana chino, sepatu casual formal'),
    ('Sales Counter', 'Senin-Kamis', 'Blouse atau kemeja formal, rok atau celana bahan, sepatu hak rendah, makeup natural'),
    ('Sales Counter', 'Jumat', 'Blouse batik atau kemeja warna soft, rok atau celana bahan, sepatu formal'),
    ('Sales Counter', 'Sabtu', 'Polo shirt atau blouse casual formal dengan logo perusahaan, celana atau rok, sepatu flat'),
    ('Kasir', 'Senin-Kamis', 'Seragam kasir standar: kemeja putih, vest hitam, celana hitam, sepatu hitam tertutup'),
    ('Kasir', 'Jumat', 'Seragam kasir dengan kemeja batik atau warna khusus hari Jumat sesuai kebijakan'),
    ('Kasir', 'Sabtu', 'Seragam kasir casual: polo shirt dengan logo, celana hitam, sepatu hitam casual');

-- =================================================================
-- INDEXES FOR PERFORMANCE
-- =================================================================

CREATE INDEX idx_car_variants_car_id ON public.car_variants(car_id);
CREATE INDEX idx_car_variants_price ON public.car_variants(price);
CREATE INDEX idx_car_variants_target_demographic ON public.car_variants(target_demographic);
CREATE INDEX idx_car_variants_use_case ON public.car_variants USING gin(to_tsvector('english', use_case));
CREATE INDEX idx_promotions_dates ON public.promotions(start_date, end_date);
CREATE INDEX idx_stock_inventory_city ON public.stock_inventory(city);
CREATE INDEX idx_stock_inventory_variant_city ON public.stock_inventory(variant_id, city);