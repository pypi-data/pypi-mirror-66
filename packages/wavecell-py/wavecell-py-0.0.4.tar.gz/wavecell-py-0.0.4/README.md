# wavecell-py

Wavecell REST API Wrapper for Python

## Example

### Send SMS (single)

```python
from wavecell import Wavecell

# Init client, using default region "ID"
w = Wavecell(sub_account_id="<SUB_ACC_ID>", api_key="<API_KEY>")

# Prepare param
p = {
    "destination": "081234567890",
    "text": "Hello World"
}

# Send sms
result = w.send_sms_single(param=p)
print(result)
```

## TODOs

- [ ] SMS API
  - [X] Send SMS (single)
  - [ ] Send SMS (batch)
  - [ ] Send SMS batch (compact)
  - [ ] Cancel scheduled SMS
  - [ ] Cancel batch of scheduled SMS
- [ ] Mobile Verification API
  - [ ] Code generation
  - [ ] Code validation

## Contributors

- Saggaf Arsyad <saggaf@nbs.co.id>