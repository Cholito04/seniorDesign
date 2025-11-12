import numpy as np
import open3d as o3d

# Parameters for grid
x_min, x_max, x_step = 4041240, 4041340, 1  # X range and step size
y_min, y_max, y_step = 10228200, 10228400, 1  # Y range and step size
z_value = 0.0  # Flat surface at z = 0

# Generate 2D grid points
x_vals = np.arange(x_min, x_max + x_step, x_step)
y_vals = np.arange(y_min, y_max + y_step, y_step)
grid_points = np.array([[x, y, z_value] for x in x_vals for y in y_vals])

# Create Open3D point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(grid_points)

# Save to PCD file
o3d.io.write_point_cloud("grid_map.pcd", pcd, write_ascii=True)

print(f"PCD file 'grid_map.pcd' generated with {len(grid_points)} points.")