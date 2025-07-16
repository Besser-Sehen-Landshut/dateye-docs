# API Documentation

## POST /setPatients

### Description

This endpoint is used to upload a patient data file. The server processes the uploaded file and returns a simple response.

### Request

- **HTTP Method**: POST
- **Endpoint**: /setPatients
- **Content Type**: multipart/form-data

#### Request Parameters


| Parameter | Type | Required | Description                                                           |
| --------- | ---- | -------- | --------------------------------------------------------------------- |
| file      | File | Yes      | The patient data file to upload. The file field must be named "file". |

The endpoint uses `upload.single("file")` middleware to handle a single file upload, so the request must include a file field with the name "file".

### Response

- **HTTP Status Code**: 200 OK
- **Content Type**: text/plain

#### Response Example:

ok
