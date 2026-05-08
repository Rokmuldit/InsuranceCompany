IF OBJECT_ID('PaidPlans', 'U') IS NULL
BEGIN
    CREATE TABLE PaidPlans(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        NAME NVARCHAR(50) NOT NULL,
        DESCRIPTION NVARCHAR(MAX) NULL,
        PAYMENT_AMOUNT DECIMAL(10,2) NOT NULL,
        PAYMENT_PERIOD NVARCHAR(50) NOT NULL
    );
END;

IF OBJECT_ID('Address', 'U') IS NULL
BEGIN
    CREATE TABLE Address(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        Region NVARCHAR(100) NOT NULL,
        City NVARCHAR(100) NOT NULL,
        Street NVARCHAR(100) NOT NULL,
        House NVARCHAR(10) NOT NULL,
        Apartment NVARCHAR(10) NULL
    );
END;

IF OBJECT_ID('PersonalData', 'U') IS NULL
BEGIN
    CREATE TABLE PersonalData(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        FirstName NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        MiddleName NVARCHAR(50) NULL,
        BirthDate DATE NOT NULL,
        PhoneNumber NVARCHAR(20) UNIQUE NOT NULL,
        ID_Address UNIQUEIDENTIFIER NOT NULL,
        CONSTRAINT FK_PersonalData_Address FOREIGN KEY (ID_Address) REFERENCES Address(ID)
    );
END;

IF OBJECT_ID('Client', 'U') IS NULL
BEGIN
    CREATE TABLE Client(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        ID_PersonalData UNIQUEIDENTIFIER NOT NULL,
        CONSTRAINT FK_Client_PersonalData FOREIGN KEY (ID_PersonalData) REFERENCES PersonalData(ID)
    );
END;

IF OBJECT_ID('Agent', 'U') IS NULL
BEGIN
    CREATE TABLE Agent(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        ID_Client UNIQUEIDENTIFIER NOT NULL,
        CONSTRAINT FK_Agent_Client FOREIGN KEY (ID_Client) REFERENCES Client(ID)
    );
END;

IF OBJECT_ID('InsuranceContract', 'U') IS NULL
BEGIN
    CREATE TABLE InsuranceContract(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        ContractAmount DECIMAL(10,2) NOT NULL,
        StartDate DATE NOT NULL,
        EndDate DATE NOT NULL,
        IsActive BIT DEFAULT 1,
        ID_Client UNIQUEIDENTIFIER NOT NULL,
        ID_Agent UNIQUEIDENTIFIER NOT NULL,
        CONSTRAINT FK_InsuranceContract_Client FOREIGN KEY (ID_Client) REFERENCES Client(ID),
        CONSTRAINT FK_InsuranceContract_Agent FOREIGN KEY (ID_Agent) REFERENCES Agent(ID)
    );
END;

IF OBJECT_ID('InsuranceEvents', 'U') IS NULL
BEGIN
    CREATE TABLE InsuranceEvents(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        EventDate DATE NOT NULL,
        IsInsuranceCase BIT NOT NULL DEFAULT 0,
        Description NVARCHAR(MAX) NULL,
        ID_InsuranceContract UNIQUEIDENTIFIER NOT NULL,
        CONSTRAINT FK_InsuranceEvents_InsuranceContract FOREIGN KEY (ID_InsuranceContract) REFERENCES InsuranceContract(ID)
    );
END;

IF OBJECT_ID('InsurancePayment', 'U') IS NULL
BEGIN
    CREATE TABLE InsurancePayment(
        ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        PaymentDate DATE NOT NULL,
        PaymentAmount DECIMAL(10,2) NOT NULL,
        ID_InsuranceContract UNIQUEIDENTIFIER NOT NULL,
        ID_InsuranceEvents UNIQUEIDENTIFIER NOT NULL,
        CONSTRAINT FK_InsurancePayment_InsuranceContract FOREIGN KEY (ID_InsuranceContract) REFERENCES InsuranceContract(ID),
        CONSTRAINT FK_InsurancePayment_InsuranceEvents FOREIGN KEY (ID_InsuranceEvents) REFERENCES InsuranceEvents(ID)
    );
END;