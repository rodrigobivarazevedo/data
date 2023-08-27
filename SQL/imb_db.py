import ibm_db

def create_transaction_james_procedure(conn):
    sql = """
    CREATE OR REPLACE PROCEDURE TRANSACTION_JAMES()
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
        SET Balance = Balance - 100
        WHERE AccountName = 'James';

        UPDATE BankAccounts
        SET Balance = Balance + 100
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
    """

    try:
        stmt = ibm_db.exec_immediate(conn, sql)
        print("Stored procedure TRANSACTION_JAMES created successfully.")
    except Exception as e:
        print("Error creating stored procedure:", e)

def main():
    conn_str = "DATABASE=your_db_name;HOSTNAME=your_host;PORT=your_port;PROTOCOL=TCPIP;UID=your_username;PWD=your_password;"
    
    try:
        conn = ibm_db.connect(conn_str, "", "")
        print("Connected to the database.")
        
        create_transaction_james_procedure(conn)
        
        ibm_db.close(conn)
        print("Connection closed.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
