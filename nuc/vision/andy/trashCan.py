# if len(approx) == 4:
#     x, y , w, h = cv2.boundingRect(approx)
#     aspectRatio = float(w)/h
#     if not(aspectRatio >= 0.95 and aspectRatio < 1.05):
#         print("Rectangle")
#         # Detect corners using Shi-Tomasi algorithm
#         zero = cv2.GaussianBlur(zero, (5, 5), 0)
#         corners = cv2.goodFeaturesToTrack(zero, maxCorners=16, qualityLevel=0.10, minDistance=100)

#         # Convert corners to integer coordinates
#         corners = np.intp(corners)

#         # Draw circles around detected corners
#         for corner in corners:
#             x, y = corner.ravel()
#             cv2.circle(zero, (x, y),10, 255, -1)

#         # What to do if mutliple blocks are aligned with each other
#         # Create new contour(s) to draw
# else:
#     print("Not a square")
#     # Detect corners using Shi-Tomasi algorithm
#     zero = cv2.GaussianBlur(zero, (5, 5), 0)
#     corners = cv2.goodFeaturesToTrack(zero, maxCorners=16, qualityLevel=0.10, minDistance=100)

#     # Convert corners to integer coordinates
#     corners = np.intp(corners)

#     twoNeighbors(corners[0],corners)

#     # Draw circles around detected corners
#     for corner in corners:
#         x, y = corner.ravel()
#         cv2.circle(zero, (x, y),10, 255, -1)

#     # What to do if mutliple blocks are touching each other
#     # Create new countor(s) to draw
#     # Iterate through every point, starting from the top, find two closest points, then see if angle and distance match up
#     # If they do, reomve them from the list of points and draw a square using them
#     # If a point is already removed, then don't draw the sqaure
# ----------------------
# x = approx.ravel()[0]
# y = approx.ravel()[1] - 5

# # Thresholding?
# _, thrash = cv2.threshold(processed_green_mask, 240 , 255, cv2.CHAIN_APPROX_NONE)
# thrash = thrash.astype(np.uint8)
