from art import tprint
import periodictable

tprint("Hello World!")

print("Isotopes of Hydrogen:")
for iso in periodictable.H:
    print(f"⦿ {iso} ({iso.name}); Mass: {iso.mass}")
