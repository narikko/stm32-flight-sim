using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;

public class FlightSimBridge : MonoBehaviour
{
    [Header("Network Configuration")]
    public int listenPort = 5005;

    [Header("Flight Dynamics")]
    public float forwardSpeed = 20.0f;
    public float turnBankingFactor = 0.6f;

    [Header("Live Telemetry Monitor")]
    public bool useKalman = true;
    public float pitchDeg;
    public float rollDeg;
    public bool isButtonPressed;

    private UdpClient _udp;
    private Thread _rxThread;
    private bool _running = false;
    private readonly object _lock = new object();

    private float _pFused, _pRaw, _rFused, _rRaw;
    private byte _btnState;
    private bool _lastBtn = false;

    // GUI Background Texture
    private Texture2D _boxBackground;

    void Start()
    {
        // Generate a dark slate background texture for the HUD
        _boxBackground = new Texture2D(1, 1);
        _boxBackground.SetPixel(0, 0, new Color(0.08f, 0.1f, 0.14f, 0.85f));
        _boxBackground.Apply();

        try
        {
            _udp = new UdpClient(listenPort);
            _running = true;
            _rxThread = new Thread(UdpReceiveWorker) { IsBackground = true };
            _rxThread.Start();
            Debug.Log($"[UDP] Listening for telemetry on port {listenPort}...");
        }
        catch (Exception ex)
        {
            Debug.LogError($"[UDP] Error: {ex.Message}");
        }
    }

    void Update()
    {
        float targetP, targetR;
        bool btn;
        lock (_lock)
        {
            targetP = useKalman ? _pFused : _pRaw;
            targetR = useKalman ? _rFused : _rRaw;
            btn     = (_btnState == 1);
        }

        // Toggle modes on rising edge of button press
        if (btn && !_lastBtn)
        {
            useKalman = !useKalman;
        }
        _lastBtn = btn;

        pitchDeg = targetP;
        rollDeg  = targetR;
        isButtonPressed = btn;

        // Aircraft motion & orientation
        float currentYaw = transform.eulerAngles.y + targetR * turnBankingFactor * Time.deltaTime;
        transform.rotation = Quaternion.Euler(-targetP, currentYaw, -targetR);
        transform.Translate(Vector3.forward * (forwardSpeed * Time.deltaTime), Space.Self);
    }

    private void UdpReceiveWorker()
    {
        IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, 0);

        while (_running)
        {
            try
            {
                byte[] data = _udp.Receive(ref remoteEP);
                if (data.Length == 21 && data[0] == 0xAA && data[1] == 0x55)
                {
                    // Payload: 4 floats + 1 button byte
                    float pf = BitConverter.ToSingle(data, 2);
                    float pr = BitConverter.ToSingle(data, 6);
                    float rf = BitConverter.ToSingle(data, 10);
                    float rr = BitConverter.ToSingle(data, 14);
                    byte  bt = data[18];

                    lock (_lock)
                    {
                        _pFused = pf; _pRaw = pr;
                        _rFused = rf; _rRaw = rr;
                        _btnState = bt;
                    }
                }
            }
            catch (SocketException) { break; }
            catch (Exception) { }
        }
    }

    void OnGUI()
    {
        GUIStyle boxStyle = new GUIStyle(GUI.skin.box)
        {
            alignment = TextAnchor.UpperLeft,
            fontSize = 17,
            fontStyle = FontStyle.Bold,
            padding = new RectOffset(16, 16, 14, 14)
        };

        if (_boxBackground != null)
        {
            boxStyle.normal.background = _boxBackground;
        }

        // Cyan for clean filtered flight, bright coral red for noisy raw accelerometer
        boxStyle.normal.textColor = useKalman 
            ? new Color(0.0f, 0.95f, 0.85f) 
            : new Color(1.0f, 0.30f, 0.30f);

        string mode = useKalman ? "MODE: 2-STATE KALMAN FILTER (STABLE)" : "MODE: RAW ACCELEROMETER (NOISY)";
        string telemetry = $"Pitch: {pitchDeg:+00.0;-00.0;00.0}°  |  Roll: {rollDeg:+00.0;-00.0;00.0}°";
        string hint = isButtonPressed ? "[Hardware Button: PRESSED]" : "Press Blue Button (PC13) to Toggle";

        string hudContent = $"{mode}\n{telemetry}\n{hint}";

        GUI.Box(new Rect(25, 25, 480, 95), hudContent, boxStyle);
    }

    void OnDestroy()
    {
        _running = false;
        if (_udp != null) _udp.Close();
        if (_rxThread != null && _rxThread.IsAlive) _rxThread.Join(200);

        if (_boxBackground != null)
        {
            Destroy(_boxBackground);
        }
    }
}