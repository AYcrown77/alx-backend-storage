-- SQL script that creates a trigger that decreases the quantity
-- of an item after adding a new order
CREATE TRIGGER items__substract__quantity
AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET items.quantity = items.quantity - NEW.number
WHERE items.name = NEW.items_name;
