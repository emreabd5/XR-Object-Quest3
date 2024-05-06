using UnityEngine;

public class AxisVisualizer : MonoBehaviour
{
    void OnDrawGizmos()
    {
        // Set the Gizmo drawing position to the GameObject's position
        Vector3 position = transform.position;

        // Draw X-axis in red
        Gizmos.color = Color.red;
        Gizmos.DrawLine(position, position + transform.right);

        // Draw Y-axis in green
        Gizmos.color = Color.green;
        Gizmos.DrawLine(position, position + transform.up);

        // Draw Z-axis in blue
        Gizmos.color = Color.blue;
        Gizmos.DrawLine(position, position + transform.forward);
    }
}
