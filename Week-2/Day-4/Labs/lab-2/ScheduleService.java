package com.healthcare.scheduler;

public class ScheduleService {
    private final DoctorRepository doctorRepository;
    private final AppointmentRepository appointmentRepository;

    public ScheduleService(DoctorRepository doctorRepository, AppointmentRepository appointmentRepository) {
        this.doctorRepository = doctorRepository;
        this.appointmentRepository = appointmentRepository;
    }

    public Appointment bookAppointment(Long doctorId) {
        Doctor doctor = doctorRepository.findDoctor(doctorId);

        if (doctor == null) {
            throw new DoctorNotFoundException("Doctor not found: " + doctorId);
        }

        if (Boolean.TRUE.equals(doctor.getAvailability())) {
            return appointmentRepository.create(doctorId);
        }

        return null;
    }
}

