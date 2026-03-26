package com.example.rest_service.validator;

import com.example.rest_service.entity.Student;
import com.example.rest_service.exception.BadRequestException;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class StudentValidator {

    public void validate(Student student) {
        if (student.reference() == null || student.reference().isEmpty()) {
            throw new BadRequestException("Student.reference cannot be null or empty");
        }
        if (student.firstName() == null || student.firstName().isEmpty()) {
            throw new BadRequestException("Student.firstName cannot be null or empty");
        }
        if (student.lastName() == null || student.lastName().isEmpty()) {
            throw new BadRequestException("Student.lastName cannot be null or empty");
        }
    }

    public void validate(List<Student> students) {
        for (Student student : students) {
            validate(student);
        }
    }
}
