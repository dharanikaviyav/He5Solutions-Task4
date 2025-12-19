CREATE DATABASE invoicehub;
USE invoicehub;

CREATE TABLE invoices (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoice_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  invoice_id INT,
  item VARCHAR(100),
  qty INT,
  price DECIMAL(10,2),
  FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);
