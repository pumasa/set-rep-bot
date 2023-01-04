def hw_add_test(set_id: str, course: str, assignment: str, due: str, time: str) -> bool or str:
# Error handling
    if set_id == False or len(set_id) != 1:
        return "Invalid set id"
    elif course == False or len(course) != 4:
        return "Invalid course"
    elif time == False or len(time) == 0:
        return "Invalid time"
    elif assignment == False or len(assignment) == 0:
        return "Invalid assignment"
    elif due == False or len(due) == 0:
        return "Invalid due date"
    else:
        return True