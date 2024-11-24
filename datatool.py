import json

def read():
  try:
    with open("userinfo.json", "r") as file:
      data = json.load(file)
  except FileNotFoundError:
    return []
  return data

def new_user(id, name, grade):
  data = read()

  data.append({
    "id": id,
    "name": name,
    "grade": grade,
    "todo_list": [],
  })
  with open("userinfo.json", "w") as file:
    json.dump(data, file, indent=2)

def update_data(id, data):
  old_data = read()
  for user in old_data:
    if user["id"] == id:
      user.update(data)
      break
  with open("userinfo.json", "w") as file:
    json.dump(data, file, indent=2)