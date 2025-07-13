# API文档

## GET /getPatients

```http
GET /getPatients HTTP/1.1
Host: xxx.example.com
Content-Type: application/json
```

### 描述

该接口用于获取患者列表。

### 请求

无需提供任何请求参数。

### 响应

响应结果是一个 `IPatient` 对象数组。每个 `IPatient` 对象包含以下字段：

```ts
interface IPatient {
  firstname: string;         // 患者的名字
  lastname: string;          // 患者的姓氏
  patientId: string;         // 患者的唯一标识符
  gender: 'M' | 'F';         // 患者性别：'M' 表示男性，'F' 表示女性
  birthday: string;          // 患者的出生日期，格式为 YYYY-MM-DD
  address: string | '';      // 患者的地址，如未提供则为空字符串
  phone: string | '';        // 患者的电话号码，如未提供则为空字符串
  email: string | '';        // 患者的电子邮箱，如未提供则为空字符串
  refractiveSurgery: 'D' | 'NONE' | 'LASIK' | 'PRK'; // 屈光手术类型：'D' 表示已诊断，'NONE' 表示无手术，'LASIK' 表示LASIK手术，'PRK' 表示PRK手术
  age: number;               // 患者年龄
  status: 'unchecked';       // 患者记录的状态
  pid: string;               // 系统中的患者唯一ID
  checkTime: number;         // 患者最后检查时间的Unix时间戳（毫秒）
  createTime: number;        // 患者记录创建时的Unix时间戳（毫秒）
  isDeleted: boolean;        // 标识患者记录是否已被删除
  updateTime: number;        // 患者记录最后更新时间的Unix时间戳（毫秒）
}
```

#### `IPatient` 接口字段说明


| **字段**            | **类型**                                  | **描述**                                                                                               |
| ------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `firstname`         | `string`                                  | 患者的名字。                                                                                           |
| `lastname`          | `string`                                  | 患者的姓氏。                                                                                           |
| `patientId`         | `string`                                  | 患者的唯一标识符。                                                                                     |
| `gender`            | `'M'` \| `'F'`                            | 患者性别。可能值：<br> `'M'`: 男性 <br> `'F'`: 女性                                                    |
| `birthday`          | `string`                                  | 患者的出生日期，格式为 YYYY-MM-DD。                                                                    |
| `address`           | `string` \| `''`                          | 患者的地址，如未提供则为空字符串。                                                                     |
| `phone`             | `string` \| `''`                          | 患者的电话号码，如未提供则为空字符串。                                                                 |
| `email`             | `string` \| `''`                          | 患者的电子邮箱，如未提供则为空字符串。                                                                 |
| `refractiveSurgery` | `'D'` \| `'NONE'` \| `'LASIK'` \| `'PRK'` | 屈光手术类型：<br> `'D'`: 已诊断 <br> `'NONE'`: 无手术 <br> `'LASIK'`: LASIK手术 <br> `'PRK'`: PRK手术 |
| `age`               | `number`                                  | 患者年龄。                                                                                             |
| `status`            | `'unchecked'`                             | 患者记录当前状态。                                                                                     |
| `pid`               | `string`                                  | 系统中的患者唯一ID。                                                                                   |
| `checkTime`         | `number`                                  | 患者最后检查时间的Unix时间戳（毫秒）。                                                                 |
| `createTime`        | `number`                                  | 患者记录创建时的Unix时间戳（毫秒）。                                                                   |
| `isDeleted`         | `boolean`                                 | 标识患者记录是否已被删除。                                                                             |
| `updateTime`        | `number`                                  | 患者记录最后更新时间的Unix时间戳（毫秒）。                                                             |

### 示例响应

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
