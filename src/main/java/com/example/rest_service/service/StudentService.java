package com.example.rest_service.service;

import com.example.rest_service.entity.Student;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StudentService {
    private final List<Student> studentsInMemory = new ArrayList<>();
    private final StudentValidator validator;

    public StudentService(StudentValidator validator) {
        this.validator = validator;
    }

    public List<Student> addStudents(List<Student> newStudents) {
        for (Student student : newStudents) {
            validator.validate(student);
        }
        studentsInMemory.addAll(newStudents);
        return studentsInMemory;
    }
}
