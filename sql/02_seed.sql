-- Sample data for UI development and tests, applied after 01_schema.sql on a
-- fresh volume. IDs are explicit so tests can reference rows directly, and
-- dates are fixed around 2026-11-11: interview rounds after that day read as
-- upcoming.
--
-- Rows are mostly typical, leaning South Florida. Edge cases carry a comment
-- directly above the row.
--
-- JSON shapes:
-- jobs.requirements is an array of skill names, which Job Match compares
-- against. applications.interview_data is {"rounds": [...]} where each round
-- may have type, scheduled_at, format, interviewers, outcome, and notes.

-- Keep accented and non-Latin text intact whatever the client defaults are
SET NAMES utf8mb4;

INSERT INTO companies (
    company_id, company_name, industry, website, city, state, notes
) VALUES
(
    1,
    'TechCorp',
    'Software',
    'https://www.techcorp.example',
    'Miami',
    'FL',
    'Product shop in Brickell. Hybrid, three days in office.'
),
(
    2,
    'DataCo',
    'Data & Analytics',
    'https://dataco.example',
    'Fort Lauderdale',
    'FL',
    'Analytics consultancy, mostly retail and hospitality clients.'
),
(
    3,
    'Harborlight Health',
    'Healthcare',
    'https://www.harborlighthealth.example',
    'Coral Gables',
    'FL',
    NULL
),
(
    4,
    'Coquina Logistics',
    'Logistics',
    'https://coquinalogistics.example',
    'Doral',
    'FL',
    'Freight forwarding near MIA. Mostly Java, slowly moving to Kotlin.'
),
(
    5,
    'Mangrove Financial',
    'Fintech',
    'https://www.mangrovefinancial.example',
    'Miami',
    'FL',
    'Payments startup, Series B. Met the team at the FIU career fair.'
),
(
    6,
    'Brightwave Learning',
    'Education Technology',
    'https://brightwave.example',
    'Orlando',
    'FL',
    NULL
),
(
    7,
    'Sunpath Energy',
    'Energy',
    'https://www.sunpathenergy.example',
    'Tampa',
    'FL',
    NULL
),
(
    8,
    'Palmetto Aerospace',
    'Aerospace',
    'https://palmettoaero.example',
    'Melbourne',
    'FL',
    'Most roles require US citizenship (ITAR).'
),
(
    9,
    'Keystone Cyber',
    'Cybersecurity',
    'https://keystonecyber.example',
    'Jacksonville',
    'FL',
    NULL
),
(
    10,
    'Orchid Hospitality Group',
    'Hospitality',
    NULL,
    'Miami Beach',
    'FL',
    'No careers page, roles only go up on job boards.'
),
(
    11,
    'Lumen Retail Co.',
    'Retail',
    'https://www.lumenretail.example',
    'Atlanta',
    'GA',
    NULL
),
(
    12,
    'Cascade Ridge Cloud',
    'Cloud Infrastructure',
    'https://cascaderidge.example',
    'Seattle',
    'WA',
    'Several teams hiring at once. Keep track of which recruiter is which.'
),
(
    13,
    'Bluebonnet Games',
    'Gaming',
    'https://bluebonnetgames.example',
    'Austin',
    'TX',
    NULL
),
(
    14,
    'Meridian Media Labs',
    'Media',
    'https://meridianmedia.example',
    'New York',
    'NY',
    NULL
),
(
    15,
    'Fogline Robotics',
    'Robotics',
    'https://foglinerobotics.example',
    'San Francisco',
    'CA',
    'Warehouse automation. Onsite five days a week.'
),
(16, 'Lakeshore Insurance', 'Insurance', NULL, 'Chicago', 'IL', NULL),
(
    17,
    'Civic Grid Labs',
    'Government Technology',
    'https://civicgrid.example',
    'Washington',
    'DC',
    NULL
),
-- Remote company: no city or state
(
    18,
    'Driftwood Software',
    'Software',
    'https://driftwood.example',
    NULL,
    NULL,
    'Fully remote and async-first. US time zones only.'
),
(
    19,
    'Maple & Pine Analytics',
    'Data & Analytics',
    'https://mapleandpine.example',
    'Toronto',
    'Ontario',
    NULL
),
-- Non-ASCII name, city, and state
(
    20,
    'Müller & Söhne Systemhaus GmbH',
    'IT Services',
    'https://www.mueller-soehne.example',
    'München',
    'Bayern',
    'Postings are in German, but the interviews can be in English.'
),
(
    21,
    'Señal Labs',
    'Telecommunications',
    'https://senal-labs.example',
    'San Juan',
    'PR',
    NULL
),
-- Name only, with no jobs or contacts: empty states and a clean delete
(22, 'Quiet Harbor Partners', NULL, NULL, NULL, NULL, NULL),
-- Every bounded column at its maximum length, plus a long unbroken paragraph
(
    23,
    'The Extraordinarily Long-Named International Consortium for Applied Research & Development Institute',  -- noqa: LT05
    'Research, Development, and Technology Transfer Svc',
    'https://www.extraordinarily-long-named-international-consortium.example/about/applied-research-and-development/locations/headquarters/visitor-information?ref=company-directory&lang=en&src=seed-data-01',  -- noqa: LT05
    'Saint-Rémy-de-Provence-sur-Mer-et-Environs-du-Nord',
    'Provence-Alpes-Côte d''Azur, Bouches-du-Rhône Dept.',
    CONCAT(
        'Found this through a research jobs newsletter. The consortium runs ',
        'labs on three continents and the posting reads like it was written ',
        'by a committee, so expect a long process with several panels and a ',
        'research talk. Benefits look strong, relocation is covered, and the ',
        'team says remote work is possible after the first year. Their ',
        'application portal times out after about twenty minutes, so draft ',
        'answers elsewhere first. Full listing: https://careers.',
        'extraordinarily-long-named-international-consortium.example/jobs/',
        'principal-interdisciplinary-research-software-engineer'
    )
),
-- Quotes, apostrophes, HTML, and a script tag: check escaping end to end
(
    24,
    'Dunn & O''Malley Consulting',
    'Consulting',
    'https://dunn-omalley.example',
    'Boca Raton',
    'FL',
    'Recruiter said to "apply through the portal", <b>not</b> by email.
Travel is up to 50% & mostly client sites — ask about per diem.
<script>alert(''xss'')</script>'
),
-- Contacts but no jobs: deleting it cascades to its contacts
(
    25,
    'Seagrape Ventures',
    'Venture Capital',
    'https://seagrape.example',
    'Miami',
    'FL',
    'Not hiring. Good for intros to portfolio companies.'
),
-- Lowercase brand name: sorting and capitalization
(26, 'nimbus studio', 'Design', 'https://nimbus.example', 'Miami', 'FL', NULL);

INSERT INTO jobs (
    job_id,
    company_id,
    job_title,
    job_type,
    salary_min,
    salary_max,
    job_url,
    date_posted,
    requirements
) VALUES
-- TechCorp (1)
-- Job Match example from the specification: Python, SQL, Flask scores 100%
(
    1,
    1,
    'Software Developer',
    'Full-time',
    85000,
    105000,
    'https://www.techcorp.example/careers/software-developer',
    '2026-10-14',
    '["Python", "SQL", "Flask"]'
),
(
    2,
    1,
    'Senior Backend Engineer',
    'Full-time',
    150000,
    180000,
    'https://www.techcorp.example/careers/senior-backend-engineer',
    '2026-09-22',
    '["Python", "PostgreSQL", "Docker", "AWS", "REST APIs"]'
),
(
    3,
    1,
    'Frontend Engineer',
    'Full-time',
    110000,
    135000,
    'https://www.techcorp.example/careers/frontend-engineer',
    '2026-10-30',
    '["JavaScript", "TypeScript", "React", "CSS"]'
),
(
    4,
    1,
    'DevOps Engineer',
    'Contract',
    120000,
    140000,
    'https://www.techcorp.example/careers/devops-engineer',
    '2026-08-05',
    '["Linux", "Terraform", "Kubernetes", "CI/CD", "AWS"]'
),
-- DataCo (2)
-- Job Match example from the specification: 67%, missing Tableau
(
    5,
    2,
    'Data Analyst',
    'Full-time',
    65000,
    80000,
    'https://dataco.example/jobs/data-analyst',
    '2026-10-20',
    '["Python", "SQL", "Tableau"]'
),
(
    6,
    2,
    'Analytics Engineer',
    'Full-time',
    95000,
    120000,
    'https://dataco.example/jobs/analytics-engineer',
    '2026-09-10',
    '["SQL", "dbt", "Python", "Snowflake", "Git"]'
),
-- Fixed pay: salary_min equals salary_max
(
    7,
    2,
    'Business Intelligence Intern',
    'Internship',
    41600,
    41600,
    'https://dataco.example/jobs/bi-intern',
    '2026-11-03',
    '["SQL", "Excel", "Power BI"]'
),
-- Harborlight Health (3)
(
    8,
    3,
    'Health Data Engineer',
    'Full-time',
    105000,
    130000,
    'https://www.harborlighthealth.example/careers/4412',
    '2026-09-29',
    '["Python", "SQL", "Spark", "HL7", "FHIR"]'
),
(
    9,
    3,
    'Clinical Systems Analyst',
    'Full-time',
    72000,
    88000,
    NULL,
    '2026-10-06',
    '["SQL", "Epic", "Communication"]'
),
-- Lower bound only
(
    10,
    3,
    'IT Support Specialist',
    'Part-time',
    38000,
    NULL,
    'https://www.harborlighthealth.example/careers/4437',
    '2026-11-07',
    '["Windows", "Active Directory", "Networking"]'
),
-- Coquina Logistics (4)
(
    11,
    4,
    'Software Engineer II',
    'Full-time',
    100000,
    125000,
    'https://coquinalogistics.example/careers/swe-2',
    '2026-08-18',
    '["Java", "Spring Boot", "Kotlin", "MySQL", "Kafka"]'
),
-- Upper bound only, and messy requirements (case, duplicates, whitespace)
-- for Job Match normalization
(
    12,
    4,
    'Operations Data Analyst',
    'Full-time',
    NULL,
    75000,
    'https://coquinalogistics.example/careers/ops-analyst',
    '2026-10-01',
    '["excel", "SQL", "sql", "Power BI", " python "]'
),
-- Mangrove Financial (5)
(
    13,
    5,
    'Backend Engineer',
    'Full-time',
    130000,
    155000,
    'https://www.mangrovefinancial.example/jobs/backend-engineer',
    '2026-08-25',
    '["Go", "PostgreSQL", "Kafka", "Docker", "gRPC"]'
),
-- No job type
(
    14,
    5,
    'Fraud Data Scientist',
    NULL,
    120000,
    150000,
    'https://www.mangrovefinancial.example/jobs/fraud-data-scientist',
    '2026-09-15',
    '["Python", "Machine Learning", "SQL", "Pandas", "scikit-learn"]'
),
(
    15,
    5,
    'QA Automation Engineer',
    'Contract',
    90000,
    110000,
    'https://www.mangrovefinancial.example/jobs/qa-automation',
    '2026-10-12',
    '["Python", "Selenium", "Playwright", "CI/CD"]'
),
(
    16,
    5,
    'Software Engineering Intern',
    'Internship',
    52000,
    62400,
    'https://www.mangrovefinancial.example/jobs/swe-intern-2027',
    '2026-10-27',
    '["Python", "Git", "SQL"]'
),
-- Brightwave Learning (6)
(
    17,
    6,
    'Full Stack Developer',
    'Full-time',
    90000,
    115000,
    'https://brightwave.example/careers/full-stack',
    '2026-09-03',
    '["JavaScript", "Node.js", "React", "MongoDB", "HTML", "CSS"]'
),
-- Unlisted salary
(
    18,
    6,
    'Instructional Technologist',
    'Part-time',
    NULL,
    NULL,
    'https://brightwave.example/careers/instructional-tech',
    '2026-10-17',
    '["Canvas LMS", "HTML", "Communication"]'
),
-- Sunpath Energy (7)
(
    19,
    7,
    'SCADA Software Engineer',
    'Full-time',
    98000,
    122000,
    'https://www.sunpathenergy.example/careers/scada',
    '2026-07-21',
    '["C#", ".NET", "SQL", "Modbus"]'
),
(
    20,
    7,
    'Data Engineer',
    'Full-time',
    110000,
    135000,
    'https://www.sunpathenergy.example/careers/data-engineer',
    '2026-10-08',
    '["Python", "Airflow", "Spark", "Azure", "SQL"]'
),
-- Palmetto Aerospace (8)
(
    21,
    8,
    'Embedded Software Engineer',
    'Full-time',
    115000,
    140000,
    'https://palmettoaero.example/jobs/embedded-swe',
    '2026-09-08',
    '["C++", "C", "RTOS", "Linux", "Git"]'
),
(
    22,
    8,
    'Flight Software Intern',
    'Internship',
    47000,
    54000,
    'https://palmettoaero.example/jobs/flight-sw-intern',
    '2026-10-22',
    '["C++", "Python", "Linux"]'
),
-- Keystone Cyber (9)
(
    23,
    9,
    'SOC Analyst I',
    'Full-time',
    62000,
    74000,
    'https://keystonecyber.example/careers/soc-analyst',
    '2026-10-02',
    '["SIEM", "Splunk", "Networking", "Linux", "Incident Response"]'
),
(
    24,
    9,
    'Penetration Tester',
    'Contract',
    115000,
    145000,
    'https://keystonecyber.example/careers/pentester',
    '2026-09-18',
    '["Penetration Testing", "Burp Suite", "Python", "Networking", "OSCP"]'
),
(
    25,
    9,
    'Security Engineering Intern',
    'Internship',
    45000,
    52000,
    'https://keystonecyber.example/careers/security-intern',
    '2026-11-05',
    '["Python", "Linux", "Networking"]'
),
-- Orchid Hospitality Group (10)
-- Job board link with tracking parameters
(
    26,
    10,
    'Salesforce Developer',
    'Contract',
    95000,
    115000,
    'https://jobs.board.example/view/8842137?utm_source=newsletter&utm_medium=email&utm_campaign=weekly-tech-roles-2026-08&utm_content=salesforce-developer&ref=orchid-hospitality-group',  -- noqa: LT05
    '2026-08-12',
    '["Salesforce", "Apex", "SOQL", "JavaScript"]'
),
-- Lumen Retail Co. (11)
-- Same title as job 3 at another company
(
    27,
    11,
    'Frontend Engineer',
    'Full-time',
    105000,
    130000,
    'https://www.lumenretail.example/careers/frontend-engineer',
    '2026-07-01',
    '["React", "TypeScript", "GraphQL", "CSS", "Jest"]'
),
(
    28,
    11,
    'Data Scientist',
    'Full-time',
    115000,
    145000,
    'https://www.lumenretail.example/careers/data-scientist',
    '2026-09-24',
    '["Python", "SQL", "Machine Learning", "A/B Testing", "Tableau"]'
),
(
    29,
    11,
    'iOS Engineer',
    'Full-time',
    120000,
    150000,
    'https://www.lumenretail.example/careers/ios-engineer',
    '2026-10-29',
    '["Swift", "SwiftUI", "Xcode", "REST APIs"]'
),
-- Cascade Ridge Cloud (12)
(
    30,
    12,
    'Site Reliability Engineer',
    'Full-time',
    145000,
    185000,
    'https://cascaderidge.example/jobs/sre',
    '2026-09-01',
    '["Linux", "Kubernetes", "Go", "Prometheus", "Terraform", "AWS"]'
),
(
    31,
    12,
    'Cloud Support Engineer',
    'Full-time',
    85000,
    105000,
    'https://cascaderidge.example/jobs/cloud-support',
    '2026-10-15',
    '["Linux", "Networking", "AWS", "Python", "Communication"]'
),
-- High salary and a long requirements list
(
    32,
    12,
    'Senior Platform Engineer',
    'Full-time',
    210000,
    285000,
    'https://cascaderidge.example/jobs/senior-platform',
    '2026-10-21',
    '[
    "Go", "Rust", "Kubernetes", "Terraform", "AWS", "GCP", "Azure",
    "Linux", "Kafka", "PostgreSQL", "Redis", "gRPC", "CI/CD", "Observability"
]'
),
(
    33,
    12,
    'Technical Writer',
    'Contract',
    NULL,
    NULL,
    'https://cascaderidge.example/jobs/technical-writer',
    '2026-11-10',
    '["Technical Writing", "Markdown", "Git", "REST APIs"]'
),
-- Bluebonnet Games (13)
(
    34,
    13,
    'Gameplay Programmer',
    'Full-time',
    95000,
    120000,
    'https://bluebonnetgames.example/jobs/gameplay-programmer',
    '2026-08-28',
    '["C#", "Unity", "Linear Algebra", "Git"]'
),
-- Empty requirements array, distinct from NULL
(
    35,
    13,
    'QA Tester',
    'Part-time',
    35000,
    42000,
    'https://bluebonnetgames.example/jobs/qa-tester',
    '2026-09-30',
    '[]'
),
-- Meridian Media Labs (14)
(
    36,
    14,
    'Full Stack Engineer',
    'Full-time',
    125000,
    155000,
    'https://meridianmedia.example/careers/full-stack',
    '2026-10-09',
    '["TypeScript", "Node.js", "React", "PostgreSQL", "AWS"]'
),
(
    37,
    14,
    'Data Visualization Developer',
    'Contract',
    100000,
    120000,
    'https://meridianmedia.example/careers/data-viz',
    '2026-10-24',
    '["JavaScript", "D3.js", "SVG", "SQL"]'
),
-- Fogline Robotics (15): jobs without any applications
(
    38,
    15,
    'Robotics Software Engineer',
    'Full-time',
    140000,
    175000,
    'https://foglinerobotics.example/jobs/robotics-swe',
    '2026-09-12',
    '["C++", "Python", "ROS", "Linux", "Computer Vision"]'
),
(
    39,
    15,
    'Machine Learning Engineer',
    'Full-time',
    160000,
    200000,
    'https://foglinerobotics.example/jobs/ml-engineer',
    '2026-10-19',
    '["Python", "PyTorch", "Machine Learning", "Docker", "CUDA"]'
),
-- Lakeshore Insurance (16)
-- Found through a referral: no link or posting date
(
    40,
    16,
    'Java Developer',
    'Full-time',
    98000,
    118000,
    NULL,
    NULL,
    '["Java", "Spring Boot", "Oracle", "SQL"]'
),
-- Stale posting from months ago
(
    41,
    16,
    'Business Systems Analyst',
    'Full-time',
    78000,
    95000,
    'https://jobs.board.example/view/7710254',
    '2026-03-02',
    '["SQL", "Excel", "Jira", "Communication"]'
),
-- Civic Grid Labs (17)
(
    42,
    17,
    'Digital Services Developer',
    'Full-time',
    97000,
    125000,
    'https://civicgrid.example/jobs/digital-services-developer',
    '2026-09-26',
    '["Python", "Django", "PostgreSQL", "Accessibility", "Git"]'
),
-- Unpaid: a zero salary is not the same as an unlisted one
(
    43,
    17,
    'Civic Tech Volunteer',
    'Part-time',
    0,
    0,
    'https://civicgrid.example/jobs/volunteer',
    '2026-10-05',
    '["HTML", "CSS", "JavaScript"]'
),
-- Driftwood Software (18)
(
    44,
    18,
    'Senior Python Engineer',
    'Full-time',
    155000,
    185000,
    'https://driftwood.example/jobs/senior-python-engineer',
    '2026-08-20',
    '["Python", "Flask", "SQL", "AWS", "Docker"]'
),
(
    45,
    18,
    'Developer Advocate',
    'Full-time',
    120000,
    140000,
    'https://driftwood.example/jobs/developer-advocate',
    '2026-10-13',
    '["Public Speaking", "Python", "JavaScript", "Technical Writing"]'
),
-- Posted today, no link, and no requirements recorded
(
    46,
    18,
    'Support Engineer',
    'Part-time',
    45000,
    55000,
    NULL,
    '2026-11-11',
    NULL
),
-- Maple & Pine Analytics (19)
(
    47,
    19,
    'Machine Learning Engineer',
    'Full-time',
    130000,
    160000,
    'https://mapleandpine.example/careers/ml-engineer',
    '2026-09-19',
    '["Python", "TensorFlow", "Machine Learning", "SQL", "GCP"]'
),
-- Müller & Söhne Systemhaus GmbH (20)
-- Non-ASCII title and skill
(
    48,
    20,
    'Softwareentwickler (m/w/d) Backend',
    'Full-time',
    65000,
    80000,
    'https://www.mueller-soehne.example/karriere/backend',
    '2026-10-16',
    '["Java", "Spring Boot", "PostgreSQL", "Deutsch (fließend)"]'
),
-- Señal Labs (21)
(
    49,
    21,
    'Network Automation Engineer',
    'Full-time',
    92000,
    115000,
    'https://senal-labs.example/careers/network-automation',
    '2026-09-21',
    '["Python", "Ansible", "Networking", "Linux"]'
),
(
    50,
    21,
    'Ingeniero/a de Datos',
    'Contract',
    80000,
    95000,
    'https://senal-labs.example/careers/ingeniero-de-datos',
    '2026-10-26',
    '["SQL", "Python", "Español", "Power BI"]'
),
-- The Extraordinarily Long-Named International Consortium (23)
-- Maximum length title and link, INT maximum salary, and long skill names
(
    51,
    23,
    'Principal Interdisciplinary Research Software Engineer, Applied Computing Systems and Data Platforms',  -- noqa: LT05
    'Full-time',
    2147483647,
    2147483647,
    'https://careers.extraordinarily-long-named-international-consortium.example/jobs/principal-interdisciplinary-research-software-engineer-applied-computing-systems-and-data-platforms/apply?utm_source=jobboard&utm_medium=listing&utm_campaign=fall-2026-hiring&utm_content=featured-role&ref=seed-data-0001',  -- noqa: LT05
    '2026-11-11',
    '[
        "Python", "Scientific Computing", "High-Performance Computing",
        "Distributed Systems", "Grant Writing", "Technical Leadership"
    ]'
),
-- Dunn & O'Malley Consulting (24)
-- Punctuation in the title
(
    52,
    24,
    'Technology Consultant – Data & AI',
    'Full-time',
    90000,
    115000,
    'https://dunn-omalley.example/careers/technology-consultant',
    '2026-10-11',
    '["SQL", "Python", "Power BI", "Client Communication"]'
),
-- Title only: every optional column is NULL
(53, 24, 'Associate Consultant', NULL, NULL, NULL, NULL, NULL, NULL),
-- nimbus studio (26)
(
    54,
    26,
    'UI/UX Designer & Front-End Developer',
    'Part-time',
    50000,
    65000,
    'https://nimbus.example/jobs/designer-developer',
    '2026-10-31',
    '["Figma", "HTML", "CSS", "JavaScript", "Accessibility"]'
);

INSERT INTO applications (
    application_id,
    job_id,
    application_date,
    status,
    resume_version,
    cover_letter_sent,
    interview_data
) VALUES
-- Upcoming onsite after two passed rounds
(1, 1, '2026-10-15', 'Interview', 'swe-general-v3', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-21T10:00:00",
        "format": "Phone",
        "interviewers": ["Marcus Bell"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-10-28T14:00:00",
        "format": "Video",
        "interviewers": ["Dana Whitfield"],
        "outcome": "Passed",
        "notes": "Live coding a Flask endpoint with a SQL join."
    },
    {
        "type": "Onsite",
        "scheduled_at": "2026-11-13T09:30:00",
        "format": "Onsite",
        "interviewers": ["Dana Whitfield", "Priya Raman"],
        "outcome": "Pending",
        "notes": "Bring a laptop. Parking validated at the front desk."
    }
]}'),
-- Rejected on the resume alone
(2, 2, '2026-09-24', 'Rejected', 'backend-v2', FALSE, NULL),
(3, 5, '2026-10-21', 'Screening', 'data-v2', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-11-12T11:00:00",
        "format": "Phone",
        "interviewers": ["Tasha Grant"],
        "outcome": "Pending"
    }
]}'),
-- A round without interviewers or format
(4, 6, '2026-09-12', 'Rejected', 'data-v1', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-09-18T13:00:00",
        "format": "Phone",
        "interviewers": ["Tasha Grant"],
        "outcome": "Passed"
    },
    {
        "type": "Take-home",
        "scheduled_at": "2026-09-25T23:59:00",
        "outcome": "Failed",
        "notes": "dbt project review. Feedback said the tests were thin."
    }
]}'),
(5, 7, '2026-11-04', 'Applied', 'intern-2027', FALSE, NULL),
(6, 8, '2026-10-01', 'Interview', 'data-v2', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-09T09:00:00",
        "format": "Phone",
        "interviewers": ["Omar Haddad"],
        "outcome": "Passed"
    },
    {
        "type": "Hiring Manager",
        "scheduled_at": "2026-10-23T15:00:00",
        "format": "Video",
        "interviewers": ["Renee Castillo"],
        "outcome": "Passed"
    },
    {
        "type": "Panel",
        "scheduled_at": "2026-11-18T13:00:00",
        "format": "Onsite",
        "interviewers": ["Renee Castillo", "Evan Sutter"],
        "outcome": "Pending"
    }
]}'),
-- No resume version recorded
(7, 9, '2026-10-07', 'Applied', NULL, FALSE, NULL),
(8, 11, '2026-08-19', 'Rejected', 'swe-general-v2', FALSE, '{"rounds": [
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-08-29T10:30:00",
        "format": "Video",
        "interviewers": ["Luis Ortega"],
        "outcome": "Failed"
    }
]}'),
(9, 12, '2026-10-02', 'Withdrawn', 'data-v2', FALSE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-10T16:00:00",
        "format": "Phone",
        "outcome": "Cancelled",
        "notes": "Withdrew, the role turned out to be mostly Excel reports."
    }
]}'),
(10, 13, '2026-08-26', 'Offer', 'backend-v3', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-09-02T11:00:00",
        "format": "Phone",
        "interviewers": ["Jordan Reyes"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-09-10T14:00:00",
        "format": "Video",
        "interviewers": ["Wei Zhang"],
        "outcome": "Passed"
    },
    {
        "type": "Onsite",
        "scheduled_at": "2026-09-24T09:00:00",
        "format": "Onsite",
        "interviewers": ["Wei Zhang", "Carla Mendes"],
        "outcome": "Passed",
        "notes": "System design on idempotent payment APIs."
    },
    {
        "type": "Final",
        "scheduled_at": "2026-10-01T16:30:00",
        "format": "Video",
        "interviewers": ["Jordan Reyes"],
        "outcome": "Passed",
        "notes": "Offer at 145k base. Decision due Nov 20."
    }
]}'),
(11, 14, '2026-09-16', 'Rejected', 'data-v2', TRUE, NULL),
-- Screening with no rounds scheduled yet: empty array, distinct from NULL
(12, 16, '2026-10-28', 'Screening', 'intern-2027', TRUE, '{"rounds": []}'),
-- No response for over two months
(13, 17, '2026-09-05', 'Applied', 'swe-general-v3', FALSE, NULL),
(14, 19, '2026-07-23', 'Rejected', 'swe-general-v1', FALSE, NULL),
(15, 20, '2026-10-09', 'Applied', 'data-v2', TRUE, NULL),
(16, 21, '2026-09-09', 'Interview', 'embedded-v1', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-09-17T10:00:00",
        "format": "Phone",
        "interviewers": ["Bobby Chen"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-10-01T13:30:00",
        "format": "Video",
        "interviewers": ["Bobby Chen"],
        "outcome": "Passed"
    },
    {
        "type": "Onsite",
        "scheduled_at": "2026-11-20T08:30:00",
        "format": "Onsite",
        "interviewers": ["Bobby Chen", "Hal Whitaker"],
        "outcome": "Pending",
        "notes": "Bring a passport for the badge (ITAR)."
    }
]}'),
-- Applied the same day it was posted
(17, 22, '2026-10-22', 'Applied', 'intern-2027', TRUE, NULL),
(18, 23, '2026-10-03', 'Screening', 'security-v1', FALSE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-14T12:00:00",
        "format": "Phone",
        "interviewers": ["Terrence Hall"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-11-17T10:00:00",
        "format": "Video",
        "interviewers": ["Mary-Kate Ashby-Lowe"],
        "outcome": "Pending"
    }
]}'),
(19, 24, '2026-09-19', 'Rejected', 'security-v1', TRUE, '{"rounds": [
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-09-30T15:00:00",
        "format": "Video",
        "interviewers": ["Mary-Kate Ashby-Lowe"],
        "outcome": "Failed",
        "notes": "They wanted someone who already has the OSCP."
    }
]}'),
-- Empty object, distinct from NULL
(20, 25, '2026-11-06', 'Applied', 'intern-2027', FALSE, '{}'),
-- Withdrawn before any interviews
(21, 26, '2026-08-14', 'Withdrawn', 'swe-general-v2', FALSE, NULL),
-- Two applications to the same job: rejected in July, reapplied in October
(22, 27, '2026-07-02', 'Rejected', 'frontend-v1', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-07-10T11:00:00",
        "format": "Phone",
        "interviewers": ["Devon Mitchell"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-07-17T14:00:00",
        "format": "Video",
        "interviewers": ["Hannah Park"],
        "outcome": "Failed",
        "notes": "Struggled with the accessibility questions. Study ARIA."
    }
]}'),
(23, 27, '2026-10-05', 'Applied', 'frontend-v2', TRUE, NULL),
-- Past round still pending: waiting on feedback
(24, 28, '2026-09-25', 'Interview', 'data-v2', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-02T10:00:00",
        "format": "Phone",
        "interviewers": ["Devon Mitchell"],
        "outcome": "Passed"
    },
    {
        "type": "Take-home",
        "scheduled_at": "2026-10-09T23:59:00",
        "outcome": "Passed"
    },
    {
        "type": "Panel",
        "scheduled_at": "2026-10-30T13:00:00",
        "format": "Video",
        "interviewers": ["Hannah Park", "Ravi Shah", "Elena Ruiz"],
        "outcome": "Pending",
        "notes": "Said to expect a decision within two weeks."
    }
]}'),
(25, 30, '2026-09-02', 'Rejected', 'backend-v3', FALSE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-09-09T12:00:00",
        "format": "Phone",
        "interviewers": ["Sofia Petrov"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-09-16T11:00:00",
        "format": "Video",
        "interviewers": ["Alex Kim"],
        "outcome": "Passed"
    },
    {
        "type": "Onsite",
        "scheduled_at": "2026-09-30T09:00:00",
        "format": "Onsite",
        "interviewers": ["Alex Kim", "Benjamin Okafor", "Chris Doyle"],
        "outcome": "Failed",
        "notes": "Incident response scenario went long."
    }
]}'),
(26, 31, '2026-10-16', 'Screening', 'swe-general-v3', FALSE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-23T10:30:00",
        "format": "Phone",
        "interviewers": ["Sofia Petrov"],
        "outcome": "Passed"
    }
]}'),
(27, 32, '2026-10-21', 'Applied', 'backend-v3', TRUE, NULL),
(28, 34, '2026-08-30', 'Rejected', 'gamedev-v1', TRUE, NULL),
(29, 35, '2026-10-01', 'Withdrawn', 'gamedev-v1', FALSE, '{"rounds": [
    {
        "type": "Hiring Manager",
        "scheduled_at": "2026-10-07T17:00:00",
        "format": "Video",
        "interviewers": ["Avery Johnson"],
        "outcome": "Passed",
        "notes": "Withdrew afterwards, the shifts conflict with classes."
    }
]}'),
(30, 36, '2026-10-10', 'Interview', 'swe-general-v3', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-17T13:00:00",
        "format": "Phone",
        "interviewers": ["Leah Fischer"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-11-12T15:30:00",
        "format": "Video",
        "interviewers": ["Leah Fischer", "Tom Becker"],
        "outcome": "Pending"
    }
]}'),
-- Application to a job with no posting date
(31, 40, '2026-10-19', 'Screening', 'swe-general-v3', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-27T09:30:00",
        "format": "Phone",
        "interviewers": ["Pat Morgan"],
        "outcome": "Passed",
        "notes": "Referral from a classmate."
    }
]}'),
-- Oldest application
(32, 41, '2026-03-04', 'Rejected', 'analyst-v1', FALSE, NULL),
(33, 42, '2026-09-28', 'Interview', 'swe-general-v3', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-06T11:00:00",
        "format": "Phone",
        "interviewers": ["Imani Brooks"],
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-10-20T14:00:00",
        "format": "Video",
        "interviewers": ["Imani Brooks"],
        "outcome": "Passed"
    },
    {
        "type": "Panel",
        "scheduled_at": "2026-11-19T14:00:00",
        "format": "Video",
        "interviewers": ["Imani Brooks", "Grace Liu"],
        "outcome": "Pending"
    }
]}'),
(34, 44, '2026-08-21', 'Offer', 'backend-v3', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-08-28T12:00:00",
        "format": "Video",
        "interviewers": ["Sam Rivera"],
        "outcome": "Passed"
    },
    {
        "type": "Take-home",
        "scheduled_at": "2026-09-04T23:59:00",
        "outcome": "Passed"
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-09-11T13:00:00",
        "format": "Video",
        "interviewers": ["Sam Rivera", "Morgan Ellis"],
        "outcome": "Passed"
    },
    {
        "type": "Final",
        "scheduled_at": "2026-09-18T15:00:00",
        "format": "Video",
        "interviewers": ["Sam Rivera"],
        "outcome": "Passed",
        "notes": "Offer at 165k base, fully remote."
    }
]}'),
(35, 45, '2026-10-14', 'Rejected', 'devrel-v1', TRUE, '{"rounds": [
    {
        "type": "Hiring Manager",
        "scheduled_at": "2026-10-29T16:00:00",
        "format": "Video",
        "interviewers": ["Morgan Ellis"],
        "outcome": "Failed"
    }
]}'),
(36, 47, '2026-09-20', 'Rejected', 'data-v2', FALSE, NULL),
(37, 48, '2026-10-18', 'Applied', 'swe-general-v3-de', TRUE, NULL),
-- Non-ASCII interviewer names and a round weeks out
(38, 49, '2026-09-23', 'Interview', 'swe-general-v3', FALSE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-01T10:00:00",
        "format": "Phone",
        "interviewers": ["Ana Lucía Torres"],
        "outcome": "Passed",
        "notes": "Entrevista en español."
    },
    {
        "type": "Technical Screen",
        "scheduled_at": "2026-10-15T11:00:00",
        "format": "Video",
        "interviewers": ["José Hernández"],
        "outcome": "Passed"
    },
    {
        "type": "Onsite",
        "scheduled_at": "2026-12-02T10:00:00",
        "format": "Onsite",
        "interviewers": ["José Hernández", "Ana Lucía Torres"],
        "outcome": "Pending"
    }
]}'),
-- Maximum length resume version on the maximum length job
(
    39,
    51,
    '2026-11-11',
    'Applied',
    'swe-general-v3-research-consortium-tailored-final2',
    TRUE,
    NULL
),
(40, 52, '2026-10-12', 'Screening', 'consulting-v1', TRUE, '{"rounds": [
    {
        "type": "Recruiter Screen",
        "scheduled_at": "2026-10-20T10:00:00",
        "format": "Phone",
        "interviewers": ["Siobhán O''Connor"],
        "outcome": "Passed",
        "notes": "Asked about travel, they said it''s closer to 30% for new hires."
    }
]}'),
-- Application to a job with every optional column NULL
(41, 53, '2026-10-25', 'Applied', NULL, FALSE, NULL),
(42, 54, '2026-11-02', 'Rejected', 'design-v1', TRUE, NULL),
(43, 10, '2026-11-10', 'Applied', 'swe-general-v3', FALSE, NULL);

INSERT INTO contacts (
    contact_id,
    company_id,
    contact_name,
    title,
    email,
    phone,
    linkedin_url,
    notes
) VALUES
-- TechCorp (1)
(
    1,
    1,
    'Dana Whitfield',
    'Engineering Manager',
    'dana.whitfield@techcorp.example',
    '(305) 555-0142',
    'https://www.linkedin.com/in/dana-whitfield-3a91b2',
    'Ran the technical screen. Cares a lot about tests.'
),
(
    2,
    1,
    'Marcus Bell',
    'Technical Recruiter',
    'marcus.bell@techcorp.example',
    '305-555-0117',
    'https://www.linkedin.com/in/marcus-bell-recruits',
    NULL
),
(
    3,
    1,
    'Priya Raman',
    'Senior Software Engineer',
    'priya.raman@techcorp.example',
    NULL,
    'https://www.linkedin.com/in/priya-raman-0c44e1',
    'FIU alum (2021). Offered to refer me.'
),
-- DataCo (2)
(
    4,
    2,
    'Tasha Grant',
    'Talent Acquisition Partner',
    'tasha.grant@dataco.example',
    '954-555-0163',
    NULL,
    NULL
),
-- Same name as contact 19 at another company
(
    5,
    2,
    'Alex Kim',
    'Analytics Manager',
    'alex.kim@dataco.example',
    NULL,
    'https://www.linkedin.com/in/alex-kim-7f20c4',
    'Met at the South Florida data meetup.'
),
-- Harborlight Health (3)
(
    6,
    3,
    'Renee Castillo',
    'Director of Data Engineering',
    'renee.castillo@harborlighthealth.example',
    '(786) 555-0131',
    'https://www.linkedin.com/in/renee-castillo-5d0b7a',
    NULL
),
(
    7,
    3,
    'Omar Haddad',
    'HR Generalist',
    'omar.haddad@harborlighthealth.example',
    '(305) 555-0100',
    NULL,
    NULL
),
-- Coquina Logistics (4)
(
    8,
    4,
    'Luis Ortega',
    'Engineering Lead',
    'lortega@coquinalogistics.example',
    '305.555.0188',
    NULL,
    NULL
),
-- Mangrove Financial (5)
-- Mixed case email
(
    9,
    5,
    'Jordan Reyes',
    'Head of Talent',
    'Jordan.Reyes@MangroveFinancial.example',
    '+1 786-555-0175',
    'https://www.linkedin.com/in/jordan-reyes-talent',
    'Sent the offer letter. Prefers texts over email.'
),
-- Shared inbox rather than a person, with plus addressing
(
    10,
    5,
    'Campus Recruiting Team',
    NULL,
    'campus+fiu@mangrovefinancial.example',
    NULL,
    NULL,
    'Shared inbox for internship applicants.'
),
(
    11,
    5,
    'Wei Zhang',
    'Staff Engineer',
    'wei.zhang@mangrovefinancial.example',
    NULL,
    'https://www.linkedin.com/in/wei-zhang-9e3f12',
    'Onsite interviewer, asked about idempotent payment APIs.'
),
-- Brightwave Learning (6)
-- Single name
(
    12,
    6,
    'Kalani',
    'People Operations',
    'kalani@brightwave.example',
    NULL,
    NULL,
    NULL
),
-- Palmetto Aerospace (8)
-- Double quotes in a name: check escaping inside form attributes
(
    13,
    8,
    'Robert "Bobby" Chen',
    'Flight Software Manager',
    'robert.chen@palmettoaero.example',
    '(321) 555-0177',
    'https://www.linkedin.com/in/bobby-chen-flightsw',
    NULL
),
-- Keystone Cyber (9)
(
    14,
    9,
    'Mary-Kate Ashby-Lowe',
    'SOC Manager',
    'mk.ashbylowe@keystonecyber.example',
    '(904) 555-0129',
    'https://www.linkedin.com/in/mary-kate-ashby-lowe',
    NULL
),
-- Phone extension
(
    15,
    9,
    'Terrence Hall',
    'Security Recruiter',
    'terrence.hall@keystonecyber.example',
    '904-555-0150 x204',
    NULL,
    NULL
),
-- Orchid Hospitality Group (10)
-- Phone only
(
    16,
    10,
    'Gabriela Souza',
    'IT Director',
    NULL,
    '(305) 555-0196',
    NULL,
    'Only reachable by phone. Call before 11am.'
),
-- Lumen Retail Co. (11)
(
    17,
    11,
    'Hannah Park',
    'Frontend Engineering Manager',
    'hannah.park@lumenretail.example',
    NULL,
    'https://www.linkedin.com/in/hannah-park-fe',
    'Said to reapply once their new design system ships.'
),
(
    18,
    11,
    'Devon Mitchell',
    'Recruiter',
    'devon.mitchell@lumenretail.example',
    '(404) 555-0172',
    NULL,
    NULL
),
-- Cascade Ridge Cloud (12): many contacts at one company
(
    19,
    12,
    'Alex Kim',
    'Site Reliability Manager',
    'alex.kim@cascaderidge.example',
    '(206) 555-0114',
    'https://www.linkedin.com/in/alex-kim-sre',
    NULL
),
(
    20,
    12,
    'Sofia Petrov',
    'University Recruiter',
    'sofia.petrov@cascaderidge.example',
    '(206) 555-0190',
    'https://www.linkedin.com/in/sofia-petrov-1b8d33',
    NULL
),
(
    21,
    12,
    'Benjamin Okafor',
    'Senior Platform Engineer',
    'ben.okafor@cascaderidge.example',
    NULL,
    'https://www.linkedin.com/in/benjamin-okafor-platform',
    'Referred me for the platform role.'
),
-- Non-Latin diacritics
(
    22,
    12,
    'Nguyễn Thị Lan',
    'Technical Program Manager',
    'lan.nguyen@cascaderidge.example',
    NULL,
    'https://www.linkedin.com/in/lan-nguyen-tpm',
    NULL
),
(
    23,
    12,
    'Chris Doyle',
    'Cloud Support Lead',
    'chris.doyle@cascaderidge.example',
    '206-555-0138',
    NULL,
    NULL
),
-- Bluebonnet Games (13)
(
    24,
    13,
    'Avery Johnson',
    'QA Lead',
    'avery.johnson@bluebonnetgames.example',
    '(512) 555-0146',
    NULL,
    'Very flexible about part-time hours.'
),
-- Fogline Robotics (15)
(
    25,
    15,
    'Zoë Lindqvist',
    'Robotics Recruiter',
    'zoe.lindqvist@foglinerobotics.example',
    '(415) 555-0123',
    'https://www.linkedin.com/in/zoe-lindqvist-robotics',
    NULL
),
-- Lakeshore Insurance (16)
-- Name only
(26, 16, 'Pat Morgan', NULL, NULL, NULL, NULL, NULL),
-- Civic Grid Labs (17)
-- Multi-line notes
(
    27,
    17,
    'Imani Brooks',
    'Engineering Director',
    'imani.brooks@civicgrid.example',
    '(202) 555-0161',
    'https://www.linkedin.com/in/imani-brooks-civictech',
    'Panel on Nov 19:
- Walk through an accessibility audit
- Bring examples of plain-language docs'
),
-- Driftwood Software (18)
(
    28,
    18,
    'Sam Rivera',
    'VP of Engineering',
    'sam@driftwood.example',
    NULL,
    'https://www.linkedin.com/in/sam-rivera-eng',
    'Async everything, usually replies on Fridays.'
),
(
    29,
    18,
    'Morgan Ellis',
    'Developer Relations Lead',
    'morgan.ellis@driftwood.example',
    NULL,
    'https://www.linkedin.com/in/morgan-ellis-devrel',
    NULL
),
-- Maple & Pine Analytics (19)
(
    30,
    19,
    'Arjun Mehta',
    'Machine Learning Lead',
    'arjun.mehta@mapleandpine.example',
    '+1 416-555-0157',
    'https://www.linkedin.com/in/arjun-mehta-ml',
    'Role needs Canadian work authorization.'
),
-- Müller & Söhne Systemhaus GmbH (20)
-- International phone format
(
    31,
    20,
    'Jürgen Weiß',
    'Teamleiter Backend',
    'j.weiss@mueller-soehne.example',
    '+49 89 99998 123',
    NULL,
    NULL
),
-- Señal Labs (21)
(
    32,
    21,
    'José Hernández',
    'Gerente de Ingeniería',
    'jose.hernandez@senal-labs.example',
    '+1 787-555-0144',
    'https://www.linkedin.com/in/jose-hernandez-senal',
    'Prefers Spanish for the first call.'
),
(
    33,
    21,
    'Ana Lucía Torres',
    'Recruiter',
    'ana.torres@senal-labs.example',
    '787-555-0121',
    NULL,
    NULL
),
-- The Extraordinarily Long-Named International Consortium (23)
-- Every bounded column at its maximum length
(
    34,
    23,
    'Maria de los Ángeles Fernández-Castellanos y Villanueva de la Torre-Montenegro, PhD, MBA, PMP, CISSP',  -- noqa: LT05
    'Senior Vice President of Global Talent Acquisition, University Partnerships and Early Career Program',  -- noqa: LT05
    'maria.fernandez-castellanos.villanueva@talent-acquisition.extraordinarily-long-consortium-hq.example',  -- noqa: LT05
    '+1 (305) 555-0199 x9',
    'https://www.linkedin.com/in/maria-de-los-angeles-fernandez-castellanos-villanueva-de-la-torre-montenegro-phd-8c1d?trk=public_profile_browsemap&originalSubdomain=us&lipi=urn-li-page-d-flagship3-profile',  -- noqa: LT05
    NULL
),
-- Dunn & O'Malley Consulting (24)
-- Apostrophe and accent in the name, ampersand in the title
(
    35,
    24,
    'Siobhán O''Connor',
    'Senior Manager, Data & AI',
    'siobhan.oconnor@dunn-omalley.example',
    '(561) 555-0109',
    'https://www.linkedin.com/in/siobhan-oconnor-data',
    NULL
),
-- Seagrape Ventures (25)
(
    36,
    25,
    'Natalie Vance',
    'Partner',
    'natalie@seagrape.example',
    '(305) 555-0185',
    'https://www.linkedin.com/in/natalie-vance-vc',
    'Offered intros to two portfolio companies hiring juniors.'
),
(
    37,
    25,
    'Diego Alvarez',
    'Associate',
    'diego@seagrape.example',
    NULL,
    'https://www.linkedin.com/in/diego-alvarez-seagrape',
    NULL
),
-- nimbus studio (26)
(
    38,
    26,
    'Rae Summers',
    'Design Director',
    'rae@nimbus.example',
    NULL,
    NULL,
    NULL
);
