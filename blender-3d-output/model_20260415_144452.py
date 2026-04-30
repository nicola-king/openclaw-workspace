import bpy
import math

# 清除默认场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 设置相机
bpy.ops.object.camera_add(location=(0, -10, 10), rotation=(math.radians(45), 0, 0))
bpy.context.scene.camera = bpy.context.active_object

# 添加灯光
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))


# 创建球体
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3, 0, 0))
sphere = bpy.context.active_object
# 设置材质
mat = bpy.data.materials.new(name="SphereMaterial")
mat.diffuse_color = (0, 0, 1, 1)
sphere.data.materials.append(mat)


# 设置渲染
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.cycles.samples = 128

# 保存 blend 文件
bpy.ops.wm.save_as_mainfile(filepath="OUTPUT_PATH")

# 渲染输出
bpy.context.scene.render.filepath = "OUTPUT_PATH.png"
bpy.ops.render.render(write_still=True)

print("✅ Blender 渲染完成！")
