CREATE EXTENSION IF NOT EXISTS "pgcrypto";
-- Função para atualizar o campo updated_at
CREATE OR REPLACE FUNCTION update_timestamp() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();  -- Atualiza o campo updated_at com a hora atual
    RETURN NEW;  -- Retorna o novo registro
END;
$$ LANGUAGE plpgsql;

-- Tabela de usuários
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Trigger para users
CREATE TRIGGER users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Tabela de veículos
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL,
    brand VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    observation TEXT,
    year INT,
    identifier VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Trigger para vehicles
CREATE TRIGGER vehicles_updated_at
BEFORE UPDATE ON vehicles
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Tabela de ordens de serviço
CREATE TABLE service_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id UUID NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- Trigger para service_orders
CREATE TRIGGER service_orders_updated_at
BEFORE UPDATE ON service_orders
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Tabela de checklists
CREATE TABLE checklists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_order_id UUID NOT NULL,

    radio BOOLEAN DEFAULT FALSE,
    speaker BOOLEAN DEFAULT FALSE,
    hubcaps BOOLEAN DEFAULT FALSE,
    spare_tire BOOLEAN DEFAULT FALSE,
    floor_mats BOOLEAN DEFAULT FALSE,
    auxiliary_lights BOOLEAN DEFAULT FALSE,
    warning_triangle BOOLEAN DEFAULT FALSE,
    lug_wrench BOOLEAN DEFAULT FALSE,
    cigarette_lighter BOOLEAN DEFAULT FALSE,
    antenna BOOLEAN DEFAULT FALSE,
    fire_extinguisher BOOLEAN DEFAULT FALSE,
    jack BOOLEAN DEFAULT FALSE,
    documents BOOLEAN DEFAULT FALSE,
    car_keys BOOLEAN DEFAULT FALSE,

    fuel_level INT CHECK (fuel_level >= 0 AND fuel_level <= 100),
    mileage INT,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_service_order FOREIGN KEY (service_order_id) REFERENCES service_orders(id) ON DELETE CASCADE
);

-- Trigger para checklists
CREATE TRIGGER checklists_updated_at
BEFORE UPDATE ON checklists
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Tabela de fotos do checklist
CREATE TABLE checklist_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    checklist_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_checklist FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE
);

-- Trigger para checklist_photos
CREATE TRIGGER checklist_photos_updated_at
BEFORE UPDATE ON checklist_photos
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Tabela de documentos da ordem de serviço
CREATE TABLE service_order_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_order_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_service_order_document FOREIGN KEY (service_order_id) REFERENCES service_orders(id) ON DELETE CASCADE
);

-- Trigger para service_order_documents
CREATE TRIGGER service_order_documents_updated_at
BEFORE UPDATE ON service_order_documents
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Tabela de serviços realizados na ordem de serviço
CREATE TABLE service_order_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_order_id UUID NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_service_order_service FOREIGN KEY (service_order_id) REFERENCES service_orders(id) ON DELETE CASCADE
);

-- Trigger para service_order_services
CREATE TRIGGER service_order_services_updated_at
BEFORE UPDATE ON service_order_services
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
