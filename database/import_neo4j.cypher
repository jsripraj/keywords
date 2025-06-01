// Clear data
MATCH (n) DETACH DELETE n;

// Create constraints
CREATE CONSTRAINT Faculty_facultyId IF NOT EXISTS
FOR (f:Faculty) REQUIRE f.id IS UNIQUE;

CREATE CONSTRAINT Institute_instituteId IF NOT EXISTS
FOR (i:Institute) REQUIRE i.id IS UNIQUE;

CREATE CONSTRAINT Keyword_keywordId IF NOT EXISTS
FOR (k:Keyword) REQUIRE k.id IS UNIQUE;

CREATE CONSTRAINT Publication_publicationId IF NOT EXISTS
FOR (p:Publication) REQUIRE p.id IS UNIQUE;

// Create faculty nodes
LOAD CSV WITH HEADERS FROM 'file:///faculty.csv' AS row
WITH row
WHERE row.id IS NOT NULL
MERGE (f:Faculty {id: row.id})
SET f.name = row.name,
    f.position = row.position,
    f.researchInterest = row.researchInterest,
    f.email = row.email,
    f.phone = row.phone,
    f.photoUrl = row.photoUrl;

// Create institute nodes
LOAD CSV WITH HEADERS FROM 'file:///institute.csv' AS row
WITH row
WHERE row.id IS NOT NULL
MERGE (i:Institute {id: row.id})
SET i.name = row.name,
    i.photoUrl = row.photoUrl;

// Create keyword nodes
LOAD CSV WITH HEADERS FROM 'file:///keyword.csv' AS row
WITH row
WHERE row.id IS NOT NULL
MERGE (k:Keyword {id: row.id})
SET k.name = row.name;

// Create publication nodes
LOAD CSV WITH HEADERS FROM 'file:///publication.csv' AS row
WITH row
WHERE row.id IS NOT NULL
CALL (row) {
    MERGE (p:Publication {id: row.id})
    SET p.title = row.title,
        p.venue = row.venue,
        p.year = toInteger(row.year),
        p.numCitations = toInteger(row.numCitations)
} IN TRANSACTIONS;

// Create faculty-institute relationships
LOAD CSV WITH HEADERS FROM 'file:///faculty_affiliation.csv' AS row
MATCH (f:Faculty {id: row.facultyId})
MATCH (i:Institute {id: row.instituteId})
MERGE (f)-[r:AFFILIATION_WITH]->(i);

// Create faculty-keyword relationships
LOAD CSV WITH HEADERS FROM 'file:///faculty_keyword.csv' AS row
CALL (row) {
    MATCH (f:Faculty {id: row.facultyId})
    MATCH (k:Keyword {id: row.keywordId})
    MERGE (f)-[r:INTERESTED_IN]->(k)
    SET r.score = toFloat(row.score)
} IN TRANSACTIONS;

// Create faculty-publication relationships
LOAD CSV WITH HEADERS FROM 'file:///faculty_publication.csv' AS row
CALL (row) {
    MATCH (f:Faculty {id: row.facultyId})
    MATCH (p:Publication {id: row.publicationId})
    MERGE (f)-[r:PUBLISH]->(p)
} IN TRANSACTIONS;

// Create publication-keyword relationships
LOAD CSV WITH HEADERS FROM 'file:///publication_keyword.csv' AS row
CALL (row) {
    MATCH (p:Publication {id: row.publicationId})
    MATCH (k:Keyword {id: row.keywordId})
    MERGE (p)-[r:LABEL_BY]->(k)
    SET r.score = toFloat(row.score)
} IN TRANSACTIONS;
