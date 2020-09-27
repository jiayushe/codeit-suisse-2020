# Clean the Floor

### Instructions
You find that cleaning the floor with the least amount of movement helps to calm your nerves. A value higher than 0 represents the dirtiness of the floor. Find out what is the least number of moves to clean the floor. 

Expose a `POST` endpoint `/clean_floor` for us to verify!

#### Input
```json5
{
  "tests": {
    "0": {
      "floor":[0, 1]
    },
    "1": {
      "floor":[1, 1]
    },
    ...
  }
}
```
#### Output Expected
```json5
{
  "answers": {
    "0": 1,
    "1": 2,
    ...
  }
}
```

### Itty Bitty Details
1. The start point is always at position 0 of the array
2. Each move traverses 1 position in the array and performs 1 action
3. There are only 2 possible actions per move:
    - If the position has **dirt level > 0** then the dirt level decreases by 1 _(Spend some time and effort to clean the floor)_
    - If the position has **dirt level = 0** then the dirt level increases by 1 _(You walked on a clean floor so you dirty it)_
4. When all values in the floor have a **dirt level = 0**, then the floor is clean!

### Examples
#### Input 1
```json5
[0, 1]
```
#### Output 1
```json5
1 Move to clean
Move 0: [0, 1]
Move 1: [0, 0] // You're done cleaning!
```

#### Input 2
```json5
[1, 1]
```
#### Output 2
```json5
2 Moves to clean
Move 0: [1, 1]
Move 1: [1, 0]
Move 2: [0, 0] // You're done cleaning!
```

Actual number of test cases given may change.
