-- SQL script that creates a trigger that decreases the quantity
-- of an item after adding a new order.
CREATE TRIGGER qty_decrease_items AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number
WHERE name = NEW.items_name;
