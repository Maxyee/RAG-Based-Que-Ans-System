# Frontend Setup

Go inside the ./STMS-Frontend

Then run 

```bash
npm install
```

After installing the package run

```bash
ng serve

# then visit url : http://localhost:4200
```


# Backend Setup

Go inside the ./STMS-Backend/src/SmartTaskManagement.Infrastructure/

```bash
# Create and apply migrations
dotnet ef migrations add InitialCreate --startup-project ../SmartTaskManagement.API

# update database
dotnet ef database update --startup-project ../SmartTaskManagement.API


```

Then go to API project folder 

```bash
# first navigate to the API project
cd ./SmartTaskManagement.API

# build the project
dotnet build

# run the project
dotnet run

# Swagger URL : http://localhost:5027/swagger/index.html
# API URL: http://localhost:5027/api/
```