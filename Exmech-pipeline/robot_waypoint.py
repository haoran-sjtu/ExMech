# Slider1
class slider1:
    """
    * Devices:    Formauto, Electric slider
    * NOTES:
    """
    slider_pre_far = (0.054141, 0.178784, 1.496892, -0.252687, 1.570793, 0.054133)  # 1. Slider far-end preparation point, Method: Prepare, Pose: Vertical
    slider_pre = (0.736805, -0.423234, 0.783607, -0.323538, 1.560141, -0.191548)  # 1. Slider tray position, Method: Prepare, Pose: Vertical
    slider_get = (0.736805, -0.372847, 1.371982, 0.214444, 1.560141, -0.191552)  # 2. Slider tray position, Method: Get, Pose: Vertical
    slider_put = (0.736805, -0.370159, 1.358210, 0.197985, 1.560141, -0.191548)  # 3. Slider tray position, Method: Place, Pose: Vertical


# Slider2
class slider2:
    """
    * Devices:    Formauto, Electric slider
    * NOTES:
    """
    slider_pre_far = (0.054141, 0.178784, 1.496892, -0.252687, 1.570793, 0.054133)  # 1. Slider far-end preparation point, Method: Prepare, Pose: Vertical
    slider_pre = (0.332772, -0.355713, 0.813125, -0.401946, 1.570789, 0.332764)  # 1. Slider tray position, Method: Prepare, Pose: Vertical
    slider_get = (0.332772, -0.297160, 1.471574, 0.197938, 1.570793, 0.332764)  # 2. Slider tray position, Method: Get, Pose: Vertical
    slider_put = (0.332772, -0.294139, 1.457962, 0.181307, 1.570789, 0.332764)  # 3. Slider tray position, Method: Place, Pose: Vertical


# Slider3
class slider3:
    """
    * Devices:    Formauto, Electric slider
    * NOTES:
    """
    slider_pre_far = (0.054141, 0.178784, 1.496892, -0.252687, 1.570793, 0.054133)  # 1. Slider far-end preparation point, Method: Prepare, Pose: Vertical
    slider_pre = (-0.148005, -0.307276, 1.004708, -0.240839, 1.554235, 0.744507)  # 1. Slider tray position, Method: Prepare, Pose: Vertical
    slider_get = (-0.148188, -0.294901, 1.476776, 0.218853, 1.554239, 0.744331)  # 2. Slider tray position, Method: Get, Pose: Vertical
    slider_put = (-0.148005, -0.291499, 1.463651, 0.202325, 1.554235, 0.744511)  # 3. Slider tray position, Method: Place, Pose: Vertical


# Ultrasonic cleaner
class Ultracleaner:
    """
    * Devices:    Ultrasonic cleaner
    * NOTES:
    """
    cleaner_pre = (-0.186794, 0.131747, 0.698215, -1.004328, 1.570796, -0.091253)  # 1. Ultrasonic cleaner preparation position, Pose: Vertical
    cleaner_pre2 = (2.889256, 0.351819, 1.168542, -0.754066, 1.570793, -0.108423)  # 1. Ultrasonic cleaner preparation position, Pose: Vertical
    cleaner_sink_pre = (2.429566, -0.443447, 0.823097, -0.286220, 1.563277, -0.724318)  # 2. Ultrasonic cleaner sink position, Method: Prepare, Pose: Vertical
    cleaner_sink_get = (2.429566, -0.402347, 1.271033, 0.120608, 1.563277, -0.724318)  # 3. Ultrasonic cleaner sink position, Method: Get, Pose: Vertical
    cleaner_sink_put = (2.429566, -0.400883, 1.257084, 0.105199, 1.563277, -0.724318)  # 4. Ultrasonic cleaner sink position, Method: Place, Pose: Vertical
    cleaner_sink_shake1 = (2.693256, -0.068693, 1.465374, 0.216975, 1.118352, -0.522749)
    cleaner_sink_shake2 = (2.421737, 0.080766, 1.770067, 0.751887, 1.590967, -0.701045)


# Dryer
class Dryer:
    """
    * Devices:    Dryer
    * NOTES:
    """
    dryer_board_prev = (-0.601161, -0.548970, 0.992853, -0.001907, 1.572311, -0.316811)  # 1. Dryer positioning board preparation position, Pose: Vertical
    dryer_board_putv = (-0.601161, -0.580344, 1.232602, 0.269208, 1.572311, -0.316811)  # 2. Dryer positioning board, Method: Place, Pose: Vertical
    dryer_board_getv = (-0.601161, -0.584511, 1.243710, 0.284485, 1.572311, -0.316815)  # 3. Dryer positioning board, Method: Get, Pose: Vertical

    dryer_board_preh_pre = (-1.517892, -0.018652, 1.802160, 1.819309, 2.458892, 0.009746)  # 4. Dryer positioning board preparation position, Pose: Horizontal
    dryer_board_preh = (-0.848556, -0.674624, 1.976300, 2.670588, 2.143929, 0.012702)  # 5. Dryer positioning board preparation position, Pose: Horizontal
    dryer_board_geth = (-0.848559, -1.067204, 1.874478, 2.961349, 2.143929, 0.012706)  # 6. Dryer positioning board, Method: Get, Pose: Horizontal
    dryer_board_puth = (-0.848556, -1.050582, 1.882074, 2.952322, 2.143929, 0.012702)  # 7. Dryer positioning board, Method: Place, Pose: Horizontal

    dryer_pre = (1.298947, 0.304043, 1.335578, -0.521520, 1.572172, -0.275120)
    dryer_put = (1.298950, 0.441001, 1.926880, -0.067176, 1.572176, -0.275124)
    dryer_get = (1.298953, 0.442272, 1.944366, -0.050964, 1.572179, -0.275128)


# Tray, pour out specimen
class Tray:
    """
    * Devices:    Tray
    * NOTES:
    """
    flip_prepare1 = (-2.188506, -0.184770, 1.269548, 1.445973, 2.208424, -0.769174)  # 1. Flip preparation position (high), Pose: Horizontal
    flip_prepare2 = (-1.960810, -0.696154, 2.340114, 3.028959, 1.980731, -0.769174)  # 1. Flip preparation position (low), Pose: Horizontal
    flip1 = (-1.960807, -0.696151, 2.340108, 3.028959, 1.980724, -0.769174)  # 2. Flip position 1, Pose: Horizontal
    flip2 = (-1.960807, -0.696151, 2.340108, 3.028959, 1.980724, -3.170794)  # 3. Flip position 2, rotate 90°, Pose: Horizontal
    shake1 = (-1.960807, -0.696151, 2.340108, 3.028959, 1.980724, -3.40794)  # 3. Shake position 1, rotate 90°, Pose: Horizontal
    shake2 = (-1.960807, -0.696151, 2.340108, 3.028959, 1.980724, -2.9)  # 3. Shake position 2, rotate 90°, Pose: Horizontal
    photograph = (-1.681898, 0.045488, 1.551645, -0.064616, 1.570789, -0.099272)  # 4. Photograph position, Pose: Vertical
    shear_recycle = (-0.456414, 0.319753, 1.961101, 0.062808, 1.572682, -0.456207)  # Shear waste recycling position


# Electronic balance
class Balance:
    """
    * Devices:    Balance
    * NOTES:
    """
    balance_pre = (-2.825829, -0.058819, 1.371480, -0.139271, 1.570796, -1.630827)  # 1. Electronic balance center, Pose: Vertical
    balance_get = (-2.830731, -0.084121, 1.700779, 0.215332, 1.570796, -1.635728)  # 2. Electronic balance center, Pose: Vertical
    balance_put = (-2.830728, -0.081090, 1.687789, 0.199306, 1.570799, -1.635728)  # 3. Electronic balance center, Pose: Vertical


# Material tester
class UTM:
    """
    * Devices:    TY Universal Material Tester - Compression Fixture
    * NOTES:
    """
    UTM_pre_far = (-2.755332, -0.145050, 1.237767, -0.184461, 1.570554, -1.560676)  # 1. Test far-end preparation position, Pose: Horizontal
    UTM_pre = (-2.702674, -0.562344, 0.640495, -0.364470, 1.570371, -1.508025)  # 2. Test preparation position, Pose: Horizontal
    fixture = (-2.702680, -0.533059, 0.754643, -0.279614, 1.570374, -1.508029)  # 3. Fixture position, Pose: Horizontal
    monitor = (3.458066, -0.449966, 2.391897, 2.845058, 1.576188, 0.023945)  # 4. Photograph position, Pose: Horizontal


class ZQ_UTM:
    """
    * Devices:    ZQ Universal Material Tester - Shear Fixture
    * NOTES:
    """
    UTM_pre_far = (-1.380472, 0.191292, 1.838319, 1.742655, 0.306148, -1.656790)  # 1. Test far-end preparation position, Pose: Horizontal
    UTM_pre = (-1.846010, -0.509734, 1.986213, 2.537267, 0.770799, -1.595229)  # 2. Test preparation position, Pose: Horizontal
    fixture = (-2.041735, -0.740620, 1.504773, 2.280380, 0.966382, -1.585465)  # 3. Fixture position, Pose: Horizontal
    monitor = (-1.925481, -0.535670, 1.999422, 2.538125, 0.850825, 0.008737)  # 4. Photograph position, Pose: Horizontal
    remove = (-2.051762, -0.758669, 1.468767, 2.262183, 0.976403, -1.585039)  # 5. Remove waste position, Pose: Horizontal
