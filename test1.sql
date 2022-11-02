CREATE TABLE runner2
                    (
                    id_runner int PRIMARY KEY,
					name character varying(100) NOT NULL,
					birth_date character varying(100) NOT NULL,
					sex CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
	                nation character varying(2)
                    );
					
SELECT * FROM runner2;