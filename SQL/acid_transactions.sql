/* You will create a stored procedure routine named TRANSACTION_ROSE which will include TCL commands like COMMIT and ROLLBACK.
Now develop the routine based on the given scenario to execute a transaction.
Scenario: Let’s buy Rose a pair of Boots from ShoeShop. So we have to update the Rose balance as well as the ShoeShop balance in the BankAccounts table. Then we also have to update Boots stock in the ShoeShop table. After Boots, let’s also attempt to buy Rose a pair of Trainers.
To create the stored procedure routine on Db2, copy the code below and paste it to the textbox of the Run SQL page. Click Run all. */

--#SET TERMINATOR @
CREATE PROCEDURE TRANSACTION_ROSE                           -- Name of this stored procedure routine
LANGUAGE SQL                                                -- Language used in this routine 
MODIFIES SQL DATA                                           -- This routine will only write/modify data in the table
BEGIN
        DECLARE SQLCODE INTEGER DEFAULT 0;                  -- Host variable SQLCODE declared and assigned 0
        DECLARE retcode INTEGER DEFAULT 0;                  -- Local variable retcode with declared and assigned 0
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION           -- Handler tell the routine what to do when an error or warning occurs
        SET retcode = SQLCODE;                              -- Value of SQLCODE assigned to local variable retcode
        
        UPDATE BankAccounts
        SET Balance = Balance-200
        WHERE AccountName = 'Rose';
        
        UPDATE BankAccounts
        SET Balance = Balance+200
        WHERE AccountName = 'Shoe Shop';
        
        UPDATE ShoeShop
        SET Stock = Stock-1
        WHERE Product = 'Boots';
        
        IF retcode < 0 THEN                                  --  SQLCODE returns negative value for error, zero for success, positive value for warning
            ROLLBACK WORK;
        
        ELSE
            COMMIT WORK;
        
        END IF;
        
END
@ 

CALL TRANSACTION_ROSE;  -- Caller query
SELECT * FROM BankAccounts;
SELECT * FROM ShoeShop;


/* The SQLCODE which is a stand-alone host variable contains success/failure/warning information of each SQL statement execution. Now since SQLCODE variable gets reset back as the next SQL statement runs, retcode is our local variable to catch the return value of this SQLCODE. SQLCODE returns negative value for each SQL statement if not executed successfully. So, on any error occurrence, all the changes are rolled back. Commit only takes place after the transaction gets executed successfully without any error.*/


/* Create a stored procedure TRANSACTION_JAMES to execute a transaction based on the following scenario: First buy James 4 pairs of Trainers from ShoeShop. Update his balance as well as the balance of ShoeShop. Also, update the stock of Trainers at ShoeShop. Then attempt to buy James a pair of Brogues from ShoeShop. If any of the UPDATE statements fail, the whole transaction fails. You will roll back the transaction. Commit the transaction only if the whole transaction is successful.*/

--#SET TERMINATOR @
CREATE PROCEDURE TRANSACTION_JAMES
LANGUAGE SQL
MODIFIES SQL DATA
BEGIN
    DECLARE SQLCODE INTEGER DEFAULT 0;
    DECLARE retcode INTEGER DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET retcode = SQLCODE;
        
    -- Buy 4 pairs of Trainers for James
    UPDATE BankAccounts
    SET Balance = Balance - (4 * 200)
    WHERE AccountName = 'James';
    
    UPDATE BankAccounts
    SET Balance = Balance + (4 * 200)
    WHERE AccountName = 'Shoe Shop';
    
    UPDATE ShoeShop
    SET Stock = Stock - 4
    WHERE Product = 'Trainers';
    
    -- Attempt to buy a pair of Brogues for James
    UPDATE BankAccounts
    SET Balance = Balance - 150
    WHERE AccountName = 'James';
    
    UPDATE BankAccounts
    SET Balance = Balance + 150
    WHERE AccountName = 'Shoe Shop';
    
    UPDATE ShoeShop
    SET Stock = Stock - 1
    WHERE Product = 'Brogues';
    
    IF retcode < 0 THEN
        ROLLBACK WORK;
    ELSE
        COMMIT WORK;
    END IF;
END
@
