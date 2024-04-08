project-name/
├── README.md
├── LICENSE
├── docker-compose.yml
├── .gitignore
├── .env
├── .env.production
├── src/
│   ├── app/
│   │   ├── controllers/   (adjusting the data before being used in the models)
│   │   ├── models/   (the business logic that routes would import to use)
│   │   └── routes/   (api routing)
│   ├── config/
│   ├── services/    (if we need to use some other external services, eg: 3rd party authorization)
│   └── utils/    (some tool funciton)
├── public/
│   ├── images/
│   ├── styles/
│   └── scripts/
├── database/
│   ├── migrations/ (CRUD things)
│   └── seeds/ (the testing data for development)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
└── scripts/
