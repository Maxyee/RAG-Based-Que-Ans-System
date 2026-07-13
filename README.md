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



```json
// appsettings.json

{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=SmartTaskManagement;Trusted_Connection=True;MultipleActiveResultSets=true",
    "DefaultConnection2": "Server=localhost\\SQLEXPRESS;Database=SmartDb;Trusted_Connection=True;MultipleActiveResultSets=true;TrustServerCertificate=True"
  },
  "JwtSettings": {
    "Secret": "YOUR-VERY-LONG-SECRET-KEY-HERE-MINIMUM-32-CHARACTERS",
    "Issuer": "SmartTaskManagement",
    "Audience": "SmartTaskManagementAPI",
    "AccessTokenExpiryMinutes": 15,
    "RefreshTokenExpiryDays": 7
  },
  "AiSettings": {
    "ApiBaseUrl": "https://models.github.ai/inference/chat/completions",
    "Model": "openai/gpt-4o-mini",
    "GitHubToken": "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",
    "DefaultTemperature": 0.7,
    "MaxTokens": 1000,
    "MaxRetries": 3,
    "TimeoutSeconds": 30,
    "EnableCaching": true,
    "CacheDurationMinutes": 60
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    }
  },
  "AllowedHosts": "*"
}

```

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