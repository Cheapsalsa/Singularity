class Resolution:
    def __init__(self, aspect, width, height, xEv, yEv, UIscale=1.0):
        self.aspect = aspect
        self.width = width
        self.height = height
        self.xEven = xEv
        self.yEven = yEv
        self.UIscale = UIscale


class Aspect:
    """
    Aspect Ratios used for mostly necessary HUD Offsets
    """

    def __init__(self, p1OF, p2OF, p3OF, p4OF, titleOF, tipOF, rectLeftOF, rectRightOF, setOF, credOF):
        # Position Offsets
        self.p1OF = p1OF
        self.p2OF = p2OF
        self.p3OF = p3OF
        self.p4OF = p4OF

        # Font Offsets
        self.titleOF = titleOF
        self.tipOF = tipOF
        self.rectLeftOF = rectLeftOF
        self.rectRightOF = rectRightOF
        self.setOF = setOF
        self.credOF = credOF


# TODO: Add / Test 4k Support
resolutions = {}

# 4:3
aspect = Aspect((0.0951, 0.294), (0.9051, 0.294), (0.0951, 0.7091), (0.9051, 0.7091), (0.1616, 0.01), (0.3275, 0.72), (0.25, 0.71), (0.5, 0.21), (0, 0), (0.71, 0.96))
resolutions['1024x768'] = Resolution(aspect, 1024, 768, 32, 24, 1.10)

aspect = Aspect((0.0825, 0.295), (0.9175, 0.295), (0.0825, 0.7095), (0.9175, 0.7095), (0.2, 0.01), (0.3475, 0.72), (0.28, 0.71), (0.445, 0.21), (0, 0), (0.74, 0.96))
resolutions['1152x768'] = Resolution(aspect, 1152, 768, 36, 24, 1.10)

aspect = Aspect((0.125, 0.30), (0.875, 0.30), (0.125, 0.70), (0.875, 0.70), (0.23, 0.01), (0.365, 0.7375), (0.3, 0.725), (0.4, 0.2125), (0, 0), (0.765, 0.965))
resolutions['1280x960'] = Resolution(aspect, 1280, 960, 40, 30, 1.10)

aspect = Aspect((0.1, 0.31), (0.9, 0.31), (0.1, 0.69), (0.9, 0.69), (0.23, 0.01), (0.365, 0.7275), (0.3, 0.715), (0.4, 0.21525), (0, 0), (0.765, 0.965))
resolutions['1280x1024'] = Resolution(aspect, 1280, 1024, 40, 32, 1.10)

# 16:9
aspect = Aspect((0.1, 0.295), (0.9, 0.295), (0.1, 0.7075), (0.9, 0.7075), (0.2275, 0.01), (0.365, 0.72), (0.3, 0.71), (0.4, 0.215), (0, 0), (0.765, 0.95))
resolutions['1280x720'] = Resolution(aspect, 1280, 720, 40, 24, 1.10)

aspect = Aspect((0.1, 0.31), (0.9, 0.31), (0.1, 0.69), (0.9, 0.69), (0.245, 0.01), (0.375, 0.72), (0.3, 0.71), (0.4, 0.215), (0, 0), (0.78, 0.955))
resolutions['1360x768'] = Resolution(aspect, 1360, 768, 40, 32, 1.10)

aspect = Aspect((0.1, 0.30), (0.9, 0.30), (0.1, 0.70), (0.9, 0.70), (0.284, 0.01), (0.3915, 0.72), (0.34, 0.71), (0.321, 0.215), (0, 0), (0.81, 0.96))
resolutions['1600x900'] = Resolution(aspect, 1600, 900, 50, 30, 1.10)

aspect = Aspect((0.105, 0.30), (0.895, 0.30), (0.105, 0.70), (0.895, 0.70), (0.25375, 0.04), (0.3825, 0.73), (0.3325, 0.72), (0.335, 0.215), (0, 0), (0.795, 0.96))
resolutions['1920x1080'] = Resolution(aspect, 1920, 1080, 48, 30, 1.40)

# 16:10
aspect = Aspect((0.1, 0.295), (0.9, 0.295), (0.1, 0.705), (0.9, 0.705), (0.2275, 0.02), (0.365, 0.72), (0.3, 0.7035), (0.4, 0.215), (0, 0), (0.763, 0.9525))
resolutions['1280x768'] = Resolution(aspect, 1280, 768, 40, 24, 1.10)

aspect = Aspect((0.1, 0.315), (0.9, 0.315), (0.1, 0.685), (0.9, 0.685), (0.2525, 0.03), (0.365, 0.72), (0.325, 0.71), (0.4, 0.215), (0, 0), (0.764, 0.9535))
resolutions['1280x800'] = Resolution(aspect, 1280, 800, 40, 32, 1.10)

aspect = Aspect((0.1, 0.285), (0.9, 0.285), (0.1, 0.715), (0.9, 0.715), (0.2825, 0.01), (0.3921, 0.72), (0.320, 0.71), (0.3625, 0.215), (0, 0), (0.811, 0.9625))
resolutions['1600x1024'] = Resolution(aspect, 1600, 1024, 50, 32, 1.10)

aspect = Aspect((0.1, 0.31), (0.9, 0.31), (0.1, 0.718), (0.9, 0.718), (0.2925, 0.07), (0.395, 0.72), (0.320, 0.71), (0.3625, 0.215), (0, 0), (0.8175, 0.9625))
resolutions['1680x1050'] = Resolution(aspect, 1680, 1050, 40, 25, 1.10)

# 21:9
aspect = Aspect((0.1125, 0.305), (0.8875, 0.305), (0.1125, 0.695), (0.8875, 0.695), (0.3055, 0.01), (0.405, 0.72), (0.3625, 0.71), (0.275, 0.215), (0, 0), (0.83225, 0.9525))
resolutions['2560x1080'] = Resolution(aspect, 2560, 1080, 80, 36, 1.525)
