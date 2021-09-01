import  re

st = 'esunny.estar.android:id/nav_tv_title'
pattern = re.compile("(^e.*):(.*)")
res = re.search(pattern, st)[1]
# res = re.sub(pattern, "abc", st)
# res = re.sub(pattern, "abc", st)

print(res)


aaa = "aaa"
aaa = aaa.replace("a", "b")
print(aaa)