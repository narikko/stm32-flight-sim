#include "kalman2d.h"

void Kalman2D_Init(Kalman2D *kf, float q_angle, float q_bias, float r_measure) {
    kf->angle = 0.0f;
    kf->bias = 0.0f;

    kf->P[0][0] = 1.0f;
    kf->P[0][1] = 0.0f;
    kf->P[1][0] = 0.0f;
    kf->P[1][1] = 1.0f;

    kf->Q_angle = q_angle;
    kf->Q_bias = q_bias;
    kf->R_measure = r_measure;
}

float Kalman2D_Update(Kalman2D *kf, float new_angle, float new_rate, float dt) {
    // 1. Predict
    float rate = new_rate - kf->bias;
    kf->angle += dt * rate;

    kf->P[0][0] += dt * (dt * kf->P[1][1] - kf->P[0][1] - kf->P[1][0] + kf->Q_angle);
    kf->P[0][1] -= dt * kf->P[1][1];
    kf->P[1][0] -= dt * kf->P[1][1];
    kf->P[1][1] += kf->Q_bias * dt;

    // 2. Innovation & Kalman Gain
    float y = new_angle - kf->angle;
    float S = kf->P[0][0] + kf->R_measure;

    float K[2];
    K[0] = kf->P[0][0] / S;
    K[1] = kf->P[1][0] / S;

    // 3. Update States
    kf->angle += K[0] * y;
    kf->bias  += K[1] * y;

    // 4. Update Covariance
    float P00_temp = kf->P[0][0];
    float P01_temp = kf->P[0][1];

    kf->P[0][0] -= K[0] * P00_temp;
    kf->P[0][1] -= K[0] * P01_temp;
    kf->P[1][0] -= K[1] * P00_temp;
    kf->P[1][1] -= K[1] * P01_temp;

    return kf->angle;
}
