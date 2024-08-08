-- SQL script that creates a trigger that decreases the quantity of an item after adding a new order.

-- Quantity in the table items can be negative.

-- Drop the trigger if it already exists to avoid conflicts
DROP TRIGGER IF EXISTS after_insert_order;

-- Create the trigger
CREATE TRIGGER after_insert_order
AFTER INSERT ON orders  -- Trigger activates after an insert into orders
FOR EACH ROW
BEGIN
    -- Update the items table by subtracting the ordered quantity
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
