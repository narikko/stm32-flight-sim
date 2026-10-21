using UnityEngine;

public class SmoothFollow : MonoBehaviour
{
    public Transform target;
    public Vector3 distanceOffset = new Vector3(0, 3.5f, -9.0f);
    public float smoothSpeed = 10.0f;

    void LateUpdate()
    {
        if (target == null) return;

        // Position camera behind aircraft local space
        Vector3 desiredPos = target.TransformPoint(distanceOffset);
        transform.position = Vector3.Lerp(transform.position, desiredPos, Time.deltaTime * smoothSpeed);

        // Keep looking slightly ahead of aircraft nose
        transform.LookAt(target.position + target.forward * 4.0f);
    }
}