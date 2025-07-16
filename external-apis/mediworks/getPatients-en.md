# API Documentation

## GET /getPatients
```http
GET /getPatients HTTP/1.1
Host: xxx.example.com
Content-Type: application/json
```

### Description

This endpoint retrieves a list of patients.

### Request

No request parameters are required.

### Response

The response is an array of `IPatient` objects. Each `IPatient` object contains the following fields:

```ts
interface IPatient {
  firstname: string;
  lastname: string;
  patientId: string;
  gender: 'M' | 'F';
  birthday: string;
  address: string | '';
  phone: string | '';
  email: string | '';
  refractiveSurgery: 'D' | 'NONE' | 'LASIK' | 'PRK';
  age: number;
  status: 'unchecked';
  pid: string;
  checkTime: number;
  createTime: number;
  isDeleted: boolean;
  updateTime: number;
}

```

#### `IPatient` Interface Fields

| **Field**           | **Type**                                    | **Description**                                                                                                        |
|---------------------|---------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `firstname`         | `string`                                    | The first name of the patient.                                                                                         |
| `lastname`          | `string`                                    | The last name of the patient.                                                                                          |
| `patientId`         | `string`                                    | The unique identifier of the patient.                                                                                  |
| `gender`            | `'M'` \| `'F'`                              | The gender of the patient. Possible values: <br> `'M'`: Male <br> `'F'`: Female                                        |
| `birthday`          | `string`                                    | The patient's date of birth in YYYY-MM-DD format.                                                                      |
| `address`           | `string` \| `''`                            | The patient's address. It can be an empty string if no address is provided.                                            |
| `phone`             | `string` \| `''`                            | The patient's phone number. It can be an empty string if no phone number is provided.                                   |
| `email`             | `string` \| `''`                            | The patient's email address. It can be an empty string if no email is provided.                                         |
| `refractiveSurgery`  | `'D'` \| `'NONE'` \| `'LASIK'` \| `'PRK'`   | The type of refractive surgery the patient has undergone, if any. Possible values: <br> `'D'`: Diagnosed <br> `'NONE'`: No surgery <br> `'LASIK'`: LASIK surgery <br> `'PRK'`: PRK surgery |
| `age`               | `number`                                    | The age of the patient.                                                                                                |
| `status`            | `'unchecked'`                               | The current status of the patient's record.                                                                            |
| `pid`               | `string`                                    | The unique patient ID in the system.                                                                                   |
| `checkTime`         | `number`                                    | The Unix timestamp (in milliseconds) of the patient's last check-in.                                                   |
| `createTime`        | `number`                                    | The Unix timestamp (in milliseconds) when the patient's record was created.                                             |
| `isDeleted`         | `boolean`                                   | A flag indicating whether the patient's record has been deleted.                                                       |
| `updateTime`        | `number`                                    | The Unix timestamp (in milliseconds) when the patient's record was last updated.                                        |

### Example Response

```json
[
  {
    "firstname": "JJ",
    "lastname": "Yang",
    "patientId": "0000000015",
    "gender": "M",
    "birthday": "2024-08-14",
    "address": "test",
    "phone": "12332111223",
    "email": "123@example.com",
    "refractiveSurgery": "D",
    "age": 0,
    "status": "unchecked",
    "pid": "7230042280986583040",
    "checkTime": 1723776407477,
    "createTime": 1723779287478,
    "isDeleted": false,
    "updateTime": 1723779287478
  },
  {
    "firstname": "Emily",
    "lastname": "Smith",
    "patientId": "0000000016",
    "gender": "F",
    "birthday": "1985-03-23",
    "address": "123 Main St",
    "phone": "5551234567",
    "email": "emily.smith@example.com",
    "refractiveSurgery": "NONE",
    "age": 39,
    "status": "checked",
    "pid": "7230042280986583041",
    "checkTime": 1723776407480,
    "createTime": 1723779287481,
    "isDeleted": false,
    "updateTime": 1723779287482
  }
]
```
