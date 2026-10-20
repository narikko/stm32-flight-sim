/*
 * kalman_filter.h
 *
 *  Created on: Nov 30, 2024
 *      Author: nh_14
 */

#ifndef INC_KALMAN2D_H_
#define INC_KALMAN2D_H_

typedef struct {
    float angle;      // Filtered angle (deg)
    float bias;       // Estimated gyro bias (deg/s)
    float P[2][2];    // Error covariance matrix
    float Q_angle;    // Process noise variance for angle
    float Q_bias;     // Process noise variance for gyro bias
    float R_measure;  // Measurement noise variance (accelerometer)
} Kalman2D;

void Kalman2D_Init(Kalman2D *kf, float q_angle, float q_bias, float r_measure);
float Kalman2D_Update(Kalman2D *kf, float new_angle, float new_rate, float dt);

#endif /* INC_KALMAN2D_H_ */
